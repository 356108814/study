static int createdir(char *file)
{
	char *pos = file;
	int len = 1;
	while (1)
	{
		pos = strchr(file + len, '/');
		if (!pos)
			break;
		*pos = 0;
		if (access(file, F_OK) != 0)
		{
			if (mkdir(file, 0755) < 0)
			{
				LOG(log_2_db_log, LOG_ERROR, "mkdir %s err %m\n", file);
				return -1;
			}
		}

		*pos = '/';
		len = pos - file + 1;
	}
	return 0;
}

static int do_bk_file(char *file, char *bfile)
{
	char curday[16] = {0x0};
	get_strtime(curday);
	char bkfile[256] = {0x0};
	snprintf(bkfile, sizeof(bkfile), "%s/%.*s/%s", logfile_bkdir, 8, curday, bfile);
	if (createdir(bkfile))
	{
		LOG(log_2_db_log, LOG_ERROR, "mkdir %s err %m\n", bkfile);
		return -1;
	}

	if(rename(file, bkfile))
	{
		LOG(log_2_db_log, LOG_ERROR, "rename %s to %s err %m\n", file, bkfile);
		return -1;
	}
	return 0;
}

static int do_err_file(char *file, char *bfile)
{
	char errfile[256] = {0x0};
	snprintf(errfile, sizeof(errfile), "%s/%s", logfile_errdir, bfile);

	if(rename(file, errfile))
	{
		LOG(log_2_db_log, LOG_ERROR, "rename %s to %s err %m\n", file, errfile);
		return -1;
	}
	return 0;
}

static int do_process_file(char *file, char *bfile, t_aimei_data_config *c)
{
	t_aimei_data_config c1;
	if (c->soname == NULL)
	{
		memset(&c1, 0, sizeof(c1));
		c1.prefix = bfile;
		if (get_soname_by_config(&c1, AIMEI_DATA_FILE_PREFIX))
		{
			LOG(log_2_db_log, LOG_ERROR, "no match so process %s %s\n", bfile, file);
			return -1;
		}
		c = &c1;
	}
	FILE *fpin = fopen(file, "r");
	if (fpin == NULL) 
	{
		LOG(log_2_db_log, LOG_ERROR, "openfile %s error %m!\n", file);
		return -1;
	}

	int ret = -1; 
	char buff[2048];
	memset(buff, 0, sizeof(buff));
	while (fgets(buff, sizeof(buff), fpin))
	{
		char *t = strrchr(buff, '\n');
		if (t)
			*t = 0x0;
		ret = call_libs(c->soname, buff);
		if (ret)
		{
			LOG(log_2_db_log, LOG_ERROR, "%s %d %s\n", __func__, __LINE__, buff);
			break;
		}
		memset(buff, 0, sizeof(buff));
	}

	fclose(fpin);
	return ret;
}

static int do_subdir(char *indir, t_aimei_data_config *c)
{
	DIR *dp;
	struct dirent *dirp;
	char fullfile[256];

	if ((dp = opendir(indir)) == NULL) 
	{
		LOG(log_2_db_log, LOG_ERROR, "opendir %s error %m!\n", indir);
		return -1;
	}

	while((dirp = readdir(dp)) != NULL) 
	{
		if (dirp->d_name[0] == '.')
			continue;
		memset(fullfile, 0, sizeof(fullfile));
		snprintf(fullfile, sizeof(fullfile), "%s/%s", indir, dirp->d_name);
		struct stat statbuf;
		if (stat(fullfile, &statbuf))
		{
			LOG(log_2_db_log, LOG_ERROR, "%s %d stat %s err %m\n", __func__, __LINE__, fullfile);
			continue;
		}

		if (S_ISDIR(statbuf.st_mode))
		{
			if (dir_recursive)
			{
				t_aimei_data_config c1;
				memset(&c1, 0, sizeof(c1));
				c1.prefix = dirp->d_name;
				if (get_soname_by_config(&c1, AIMEI_DATA_DIR_PREFIX))
				{
					LOG(log_2_db_log, LOG_ERROR, "%s %d no match so process %s\n", __func__, __LINE__, c1.prefix);
					continue;
				}
				do_subdir(fullfile, &c1);
			}
			continue;
		}
		LOG(log_2_db_log, LOG_NORMAL, "process %s\n", fullfile);
		if (do_process_file(fullfile, dirp->d_name, c))
		{
			do_err_file(fullfile, dirp->d_name);
			mydb_rollback(mysql);
		}
		else
		{
			do_bk_file(fullfile, dirp->d_name);
			mydb_commit(mysql);
		}
	}
	closedir(dp);
	return 0;
}

