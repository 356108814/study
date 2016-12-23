# 默认是提交到集群执行，input和output路径为hdfs的路径

hadoop jar /opt/hadoop-2.7.3/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar \
    -input /weather/one/ \
    -output /weather/output/one \
    -mapper ~/github/study/HadoopStudy/src/com/dream/streaming/mapper.py \
    -reducer ~/github/study/HadoopStudy/src/com/dream/streaming/reducer.py \
    -file ~/github/study/HadoopStudy/src/com/dream/streaming/mapper.py \
    -file ~/github/study/HadoopStudy/src/com/dream/streaming/reducer.py
