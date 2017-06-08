/**
 * 首页js
 */
$(function () {
    var editor = new StreamDiagramEditor(
        {
            name: 111,
            onNodeClick: function (node, nodeData) {
                var type = nodeData.type;
                //更新属性页面iframe
                var nodePropertyUrlMap = {
                    source: 'property/source.html',
                    transform: 'property/transform.html',
                    action: 'property/action.html'
                };
                $('#propertyIFrame').attr('src', nodePropertyUrlMap[type]);
                // alert(node);
            }
        }
    );
    var links = [
        {from: "i0", to: "i1"},
        {from: "i1", to: "i11"},
        {from: "i1", to: "i12"},
        {from: "i0", to: "i2"},
        {from: "i2", to: "i21"},
        {from: "i0", to: "i3"}
    ];
    var nodes = [
        {id: 'i0'},
        {id: 'i1'},
        {id: 'i11'},
        {id: 'i12'},
        {id: 'i2'},
        {id: 'i21'},
        {id: 'i3'}
    ];
    // editor.loadNodes(nodes);
    // editor.loadLinks(links);
    // editor.autoLayout();
    // editor.addNode({id: '1111'});

    //左边区域的draggable事件
    $(".tpl").each(function(){
        // alert($(this).text())
        $(this).draggable({
            helper: "clone",
            scope: "tpl"
        });
    });

    //中间拖拽区的drop事件
    $(".container").droppable({
        scope: "tpl",
        drop: function (event, ui) {
            console.log(event);
            var dropOffset = ui.offset;//坐标相对于屏幕左上角(0,0)
            var ele = ui.draggable[0];
            var type = $(ele).attr("type");
            var nodeClassMap = {
                source: 'node-source',
                transform: 'node-transform',
                action: 'node-action'
            };
            var nodeNameMap = {
                source: '数据源',
                transform: '转换',
                action: '输出'
            };

            var realOffset = getRealOffset($(ele).offset(), dropOffset);
            var node = {
                name: nodeNameMap[type],
                type: type,
                offset: {top: realOffset.top, left: realOffset.left},
                nodeClass: nodeClassMap[type]
            };

            editor.addNode(node);
        }
    });

    // $('.easyui-tabs').tabs({
    //     width: $(".easyui-tabs").parent().width(),
    //     height: "auto"
    // });

    // $('#tabs').tabs({
    //     width: $("#tabs").parent().width(),
    //     height: "auto"
    // });

    /**
     * 获取节点真实坐标
     * @param tplOffset 模板坐标
     * @param dropOffset 放下坐标
     * @returns {{top: number, left: *}}
     */
    function getRealOffset(tplOffset, dropOffset) {
        //dropOffset坐标相对于左上角(0,0),node节点坐标是相对于region center的左上角
        var northRegionHeight = $('#northRegion').height();
        var westRegionWidth = $('#westRegion').width();
        var centerRegionTitleHeight = 28;
        //图形原点距离屏幕顶部距离
        var originOffsetTop = northRegionHeight + centerRegionTitleHeight;
        //拖动的ele的offset是相对于container-tpl左上角的
        var marginTop = tplOffset.top - originOffsetTop;
        var marginLeft = tplOffset.left;
        console.log("marginTop:" + marginTop);
        console.log("marginLeft:" + marginLeft);
        console.log("originOffsetTop:" + originOffsetTop);
        console.log("westWidth:" + westRegionWidth);
        console.log('offset:top:' + dropOffset.top + ",left:" + dropOffset.left);
        //转换为节点在diagram中的真实坐标
        var realTop = dropOffset.top - originOffsetTop + marginTop;
        var realLeft = dropOffset.left - westRegionWidth + marginLeft;
        return {top: realTop, left: realLeft}
    }

    console.log(editor.nodeCount);
    console.log(editor.nodeDataMap);

});