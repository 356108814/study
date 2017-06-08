/**
 * 默认数据
 * Created by dream on 2017-6-8.
 */
(function () {
    var NodeType = window.NodeType = {};
    var Tpl = window.Tpl = {};

    //节点类型
    NodeType.source = 'source';
    NodeType.transform = 'transform';
    NodeType.action = 'action';

    //模板
    Tpl.map = {
        node: "<div id='{{id}}' class='node {{nodeClass}}' style='top: {{top}}px;left: {{left}}px;'>{{name}}</div>",
    }
})();
