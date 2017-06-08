/**
 * 流图编辑器
 */
(function () {
    var root = this;
    var StreamDiagramEditor = window.StreamDiagramEditor = function (_defaults) {
        var self = this;
        this.Defaults = {
            plumb: null,
            onNodeClick: null
        };
        if (_defaults) {
            $.extend(this.Defaults, _defaults);
        }
        console.log(this.Defaults);

        this.plumb = this.Defaults['plumb'];
        this.diagram = $('.diagram');
        this.nodeCount = 0;
        this.nodeDataMap = {};
        if (!this.plumb) {
            this.plumb = jsPlumb.getInstance({
                DragOptions: {cursor: 'pointer', zIndex: 2000},
                PaintStyle: {stroke: "#00BFFF", strokeWidth: 3},
                HoverPaintStyle: {stroke: "red", cursor: 'pointer'},
                Connector: 'Flowchart',
                Anchors: ["AutoDefault"],
                // Anchors: ["TopCenter", "TopCenter"],
                Overlays: [["Arrow", {location: 1, width: 10, length: 10}]],
                Container: this.diagram
            });
        }

        console.log(this.plumb);

        /**
         * 新加一个节点
         * @param nodeData
         */
        this.addNode = function (nodeData) {
            if(!nodeData) {
                return;
            }
            var id;
            if('id' in nodeData) {
                id = nodeData.id;
            } else {
                id = "temp_node_" + this.nodeCount + 1;
                nodeData.id = id;
            }
            var name;
            if('name' in nodeData) {
                name = nodeData.name;
            } else {
                name = "节点" + id;
                nodeData.name = name;
            }
            var offset;
            if('offset' in nodeData) {
                offset = nodeData.offset;
            } else {
                offset = {top: 0, left: 0};
                nodeData.offset = offset;
            }
            if(!'nodeClass' in nodeData) {
                nodeData.nodeClass = "";
            }
            // var nodeTpl = "<div id='{{id}}' class='node {{nodeClass}}' style='top: {{top}}px;left: {{left}}px;'>{{name}}</div>";
            var nodeTpl = Tpl.map['node'];
            var render = template.compile(nodeTpl);
            var html = render({
                id: id,
                name: name,
                top: offset.top,
                left: offset.left,
                nodeClass: nodeData.nodeClass
            });
            self.diagram.append(html);
            self.plumb.draggable(id);

            //连接终点设置
            var defaultDropOptions = {
                tolerance: "touch",
                hoverClass: "dropHover",
                activeClass: "dragActive"
            };
            var defaultEndpoint = {
                // endpoint: "Rectangle",
                // paintStyle: { width: 25, height: 21, fill: exampleColor },
                isSource: true,
                reattach: true,
                // scope: "blue",
                // connectorStyle: {
                //     gradient: {stops: [
                //         [0, exampleColor],
                //         [0.5, "#09098e"],
                //         [1, exampleColor]
                //     ]},
                //     strokeWidth: 5,
                //     stroke: exampleColor,
                //     dashstyle: "2 2"
                // },
                isTarget: true,
                beforeDrop: function (params) {
                    console.log("Connect " + params.sourceId + " to " + params.targetId + "?");
                    // return confirm("Connect " + params.sourceId + " to " + params.targetId + "?");
                    return true;
                },
                dropOptions: defaultDropOptions
            };

            //每个节点最多4个锚点
            var maxEd = 4;
            for (var i = 0; i < maxEd; i++) {
                self.plumb.addEndpoint(id, {
                    anchor: ["Perimeter", {
                        shape: "Square",
                        anchorCount: 150
                    }]
                }, defaultEndpoint);
            }

            //动态添加的要动态绑定事件
            $('#'+id).on('dblclick', function () {
                _nodeClickHandler(this, nodeData);
            });
            this.nodeDataMap[nodeData.id] = nodeData;
            this.nodeCount++;
        };

        /**
         * 删除节点
         * @param node
         */
        this.deleteNode = function (node) {
            var id = node.id;
            self.plumb.remove($('#' + id));
        };

        /**
         * 加载节点
         * @param nodes
         */
        this.loadNodes = function (nodes) {
            if (nodes instanceof Array) {
                $.each(nodes, function (index, node, array) {
                    self.addNode(node);
                });
            } else {
                console.log('nodes必须为数组');
            }
        };

        /**
         * 加载节点连线
         * @param links
         */
        this.loadLinks = function (links) {
            if (links instanceof Array) {
                _.each(links, function (link) {
                    self.plumb.connect({
                        source: link.from,
                        target: link.to,
                        // connector: ["Flowchart",
                        //     {
                        //         cornerRadius: 3,
                        //         stub: 16
                        //     }
                        // ],
                        //默认动态锚点
                        anchor: "AutoDefault"
                    });
                });
            }
        };

        /**
         * 图节点自动布局
         */
        this.autoLayout = function () {
            var dg = new dagre.graphlib.Graph();
            dg.setGraph({nodesep: 30, ranksep: 30, marginx: 50, marginy: 50});
            dg.setDefaultEdgeLabel(function () {
                return {};
            });
            $(".diagram .node").each(
                function (idx, node) {
                    var $n = $(node);
                    var box = {
                        width: Math.round($n.outerWidth()),
                        height: Math.round($n.outerHeight())
                    };
                    dg.setNode($n.attr('id'), box);
                }
            );
            self.plumb.getAllConnections()
                .forEach(function (edge) {
                    dg.setEdge(edge.source.id, edge.target.id);
                });
            dagre.layout(dg);
            var graphInfo = dg.graph();
            dg.nodes().forEach(
                function (n) {
                    var node = dg.node(n);
                    var top = Math.round(node.y - node.height / 2) + 'px';
                    var left = Math.round(node.x - node.width / 2) + 'px';
                    $('#' + n).css({left: left, top: top});
                });
            self.plumb.repaintEverything();
        };

        /**
         * 初始化
         * @private
         */
        var _init = function () {
            // _enablePanzoon();
            // _enableDraggable();
            //启用拖动
            self.plumb.draggable($(".diagram .node"));
            _bindEvent();

        };

        /**
         * 启用移动缩放
         * @private
         */
        var _enablePanzoon = function () {
            var minScale = 0.4;
            var maxScale = 2;
            var incScale = 0.1;
            var $panzoom;
            var $container = $(".container");
            _.defer(function () {
                $panzoom = $container.find('.panzoom').panzoom({
                    minScale: minScale,
                    maxScale: maxScale,
                    increment: incScale,
                    disablePan: false,
                    disableZoom: false,
                    cursor: "",
                    ignoreChildrensEvents: true
                }).on("panzoomstart", function (e, pz, ev) {
                        $panzoom.css("cursor", "move");
                    })
                    .on("panzoomend", function (e, pz) {
                        $panzoom.css("cursor", "");
                    });
                $panzoom.parent()
                    .on('mousewheel.focal', function (e) {
                        if (e.ctrlKey || e.originalEvent.ctrlKey) {
                            e.preventDefault();
                            var delta = e.delta || e.originalEvent.wheelDelta;
                            var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
                            $panzoom.panzoom('zoom', zoomOut, {
                                animate: true,
                                exponential: false,
                            });
                        } else {
                            e.preventDefault();
                            var deltaY = e.deltaY || e.originalEvent.wheelDeltaY || (-e.originalEvent.deltaY);
                            var deltaX = e.deltaX || e.originalEvent.wheelDeltaX || (-e.originalEvent.deltaX);
                            $panzoom.panzoom("pan", deltaX / 2, deltaY / 2, {
                                animate: true,
                                relative: true,
                            });
                        }
                    })
                    .on("mousedown touchstart", function (ev) {
                        var matrix = $container.find(".panzoom").panzoom("getMatrix");
                        var offsetX = matrix[4];
                        var offsetY = matrix[5];
                        var dragstart = {x: ev.pageX, y: ev.pageY, dx: offsetX, dy: offsetY};
                        $(ev.target).css("cursor", "move");
                        $(this).data('dragstart', dragstart);
                    })
                    .on("mousemove touchmove", function (ev) {
                        var dragstart = $(this).data('dragstart');
                        if (dragstart) {
                            var deltaX = dragstart.x - ev.pageX;
                            var deltaY = dragstart.y - ev.pageY;
                            var matrix = $container.find(".panzoom").panzoom("getMatrix");
                            matrix[4] = parseInt(dragstart.dx) - deltaX;
                            matrix[5] = parseInt(dragstart.dy) - deltaY;
                            $container.find(".panzoom").panzoom("setMatrix", matrix);
                        }
                    })
                    .on("mouseup touchend touchcancel", function (ev) {
                        $(this).data('dragstart', null);
                        $(ev.target).css("cursor", "");
                    });
            });
        };

        /**
         * 启用节点拖拽
         * @private
         */
        var _enableDraggable = function () {
            var currentScale = 1;
            $(".diagram .node").draggable({
                start: function (e) {
                    var pz = $(".panzoom");
                    //如果启用了panzoom缩放
                    var matrix = pz.panzoom("getMatrix");
                    if (matrix) {
                        currentScale = matrix[0];
                    }
                    $(this).css("cursor", "move");
                    pz.panzoom("disable");
                },
                drag: function (e, ui) {
                    ui.position.left = ui.position.left / currentScale;
                    ui.position.top = ui.position.top / currentScale;
                    if ($(this).hasClass("jsplumb-connected")) {
                        self.plumb.repaint($(this).attr('id'), ui.position);
                    }
                },
                stop: function (e, ui) {
                    var nodeId = $(this).attr('id');
                    if ($(this).hasClass("jsplumb-connected")) {
                        self.plumb.repaint(nodeId, ui.position);
                    }
                    $(this).css("cursor", "");
                    $(".panzoom").panzoom("enable");
                }
            });
        };

        var _nodeClickHandler = function (node, nodeData) {
            var currentNode = node;
            //当前的添加选中样式，其他的取消
            $(".diagram .node").each(function (idx, node) {
                $(node).removeClass("node-selected");
            });
            $(currentNode).addClass("node-selected");
            console.log(currentNode);

            var fun = self.Defaults['onNodeClick'];
            if(fun) {
                fun(currentNode, nodeData);
            }
        };

        /**
         * 绑定节点、连线等点击事件
         * @private
         */
        var _bindEvent = function () {
            //连线绑定点击事件，默认删除连线
            self.plumb.bind("dblclick", function (link, originalEvent) {
                console.log(link.sourceId + "->" + link.targetId);
                self.plumb.deleteConnection(link);
            });

            //节点双击
            // $('.diagram .node').on('dblclick ', function (e) {
            //     var currentNode = e.currentTarget;
            //     //当前的添加选中样式，其他的取消
            //     $(".diagram .node").each(function (idx, node) {
            //         $(node).removeClass("node-selected");
            //     });
            //     $(currentNode).addClass("node-selected");
            //     console.log(currentNode);
            // });

            //移动
            self.plumb.bind("connectionMoved", function (info, originalEvent) {
                //  only remove here, because a 'connection' event is also fired.
                // in a future release of jsplumb this extra connection event will not
                // be fired.
                console.log(info.connection);
                // updateConnections(info.connection, true);
            });

            //分离删除
            self.plumb.bind("connectionDetached", function (info, originalEvent) {
                console.log("connectionDetached:" + info.connection);
            });

        };

        _init();

        // var links = [
        //     {from: "i0", to: "i1"},
        //     {from: "i1", to: "i11"},
        //     {from: "i1", to: "i12"},
        //     {from: "i0", to: "i2"},
        //     {from: "i2", to: "i21"},
        //     {from: "i0", to: "i3"},
        // ];
        // //初始化连线
        // _.each(links, function (link) {
        //     self.plumb.connect({
        //         source: link.from,
        //         target: link.to,
        //         connector: ["Flowchart",
        //             {
        //                 cornerRadius: 3,
        //                 stub: 16
        //             }
        //         ],
        //         endpoints: ["Blank", "Blank"],
        //         overlays: [["Arrow", {location: 1, width: 10, length: 10}]],
        //     });
        // });
        // //自动排列
        // var minScale = 0.4;
        // var maxScale = 2;
        // var incScale = 0.1;
        // var $container = $(".container");
        // $diagram = $container.find(".diagram");
        // var $panzoom = null;
        // var dg = new dagre.graphlib.Graph();
        // dg.setGraph({nodesep: 30, ranksep: 30, marginx: 50, marginy: 50});
        // dg.setDefaultEdgeLabel(function () {
        //     return {};
        // });
        // $(".item").each(
        //     function (idx, node) {
        //         var $n = $(node);
        //         var box = {
        //             width: Math.round($n.outerWidth()),
        //             height: Math.round($n.outerHeight())
        //         };
        //         dg.setNode($n.attr('id'), box);
        //     }
        // );
        // this.plumb.getAllConnections()
        //     .forEach(function (edge) {
        //         dg.setEdge(edge.source.id, edge.target.id);
        //     });
        // dagre.layout(dg);
        // var graphInfo = dg.graph();
        // dg.nodes().forEach(
        //     function (n) {
        //         var node = dg.node(n);
        //         var top = Math.round(node.y - node.height / 2) + 'px';
        //         var left = Math.round(node.x - node.width / 2) + 'px';
        //         $('#' + n).css({left: left, top: top});
        //     });
        // this.plumb.repaintEverything();
        //
        // _.defer(function () {
        //     $panzoom = $container.find('.panzoom').panzoom({
        //         minScale: minScale,
        //         maxScale: maxScale,
        //         increment: incScale,
        //         disablePan: false,
        //         disableZoom: false,
        //         cursor: "",
        //         ignoreChildrensEvents: true
        //     }).on("panzoomstart", function (e, pz, ev) {
        //             $panzoom.css("cursor", "move");
        //         })
        //         .on("panzoomend", function (e, pz) {
        //             $panzoom.css("cursor", "");
        //         });
        //     $panzoom.parent()
        //         .on('mousewheel.focal', function (e) {
        //             if (e.ctrlKey || e.originalEvent.ctrlKey) {
        //                 e.preventDefault();
        //                 var delta = e.delta || e.originalEvent.wheelDelta;
        //                 var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
        //                 $panzoom.panzoom('zoom', zoomOut, {
        //                     animate: true,
        //                     exponential: false,
        //                 });
        //             } else {
        //                 e.preventDefault();
        //                 var deltaY = e.deltaY || e.originalEvent.wheelDeltaY || (-e.originalEvent.deltaY);
        //                 var deltaX = e.deltaX || e.originalEvent.wheelDeltaX || (-e.originalEvent.deltaX);
        //                 $panzoom.panzoom("pan", deltaX / 2, deltaY / 2, {
        //                     animate: true,
        //                     relative: true,
        //                 });
        //             }
        //         })
        //         .on("mousedown touchstart", function (ev) {
        //             var matrix = $container.find(".panzoom").panzoom("getMatrix");
        //             var offsetX = matrix[4];
        //             var offsetY = matrix[5];
        //             var dragstart = {x: ev.pageX, y: ev.pageY, dx: offsetX, dy: offsetY};
        //             $(ev.target).css("cursor", "move");
        //             $(this).data('dragstart', dragstart);
        //         })
        //         .on("mousemove touchmove", function (ev) {
        //             var dragstart = $(this).data('dragstart');
        //             if (dragstart) {
        //                 var deltaX = dragstart.x - ev.pageX;
        //                 var deltaY = dragstart.y - ev.pageY;
        //                 var matrix = $container.find(".panzoom").panzoom("getMatrix");
        //                 matrix[4] = parseInt(dragstart.dx) - deltaX;
        //                 matrix[5] = parseInt(dragstart.dy) - deltaY;
        //                 $container.find(".panzoom").panzoom("setMatrix", matrix);
        //             }
        //         })
        //         .on("mouseup touchend touchcancel", function (ev) {
        //             $(this).data('dragstart', null);
        //             $(ev.target).css("cursor", "");
        //         });
        // });
        // //设置节点拖动
        // var currentScale = 1;
        // $container.find(".diagram .item").draggable({
        //     start: function (e) {
        //         var pz = $container.find(".panzoom");
        //         currentScale = pz.panzoom("getMatrix")[0];
        //         $(this).css("cursor", "move");
        //         pz.panzoom("disable");
        //     },
        //     drag: function (e, ui) {
        //         ui.position.left = ui.position.left / currentScale;
        //         ui.position.top = ui.position.top / currentScale;
        //         if ($(this).hasClass("jsplumb-connected")) {
        //             self.plumb.repaint($(this).attr('id'), ui.position);
        //         }
        //     },
        //     stop: function (e, ui) {
        //         var nodeId = $(this).attr('id');
        //         if ($(this).hasClass("jsplumb-connected")) {
        //             self.plumb.repaint(nodeId, ui.position);
        //         }
        //         $(this).css("cursor", "");
        //         $container.find(".panzoom").panzoom("enable");
        //     }
        // });
    };

    // window.StreamDiagramEditor = {
    //     constructor : function() {
    //         this.version = "1.0";
    //         alert(111);
    //     },
    //     init: function () {
    //         var minScale = 0.4;
    //         var maxScale = 2;
    //         var incScale = 0.1;
    //         // var plumb = null;
    //         var $container = $(".container");
    //         $diagram = $container.find(".diagram");
    //         var $panzoom = null;
    //         var links = [
    //             {from: "i0", to: "i1"},
    //             {from: "i1", to: "i11"},
    //             {from: "i1", to: "i12"},
    //             {from: "i0", to: "i2"},
    //             {from: "i2", to: "i21"},
    //             {from: "i0", to: "i3"},
    //         ];
    //
    //         jsPlumb.ready(function () {
    //             plumb = jsPlumb.getInstance({
    //                 PaintStyle: {strokeWidth: 1},
    //                 Anchors: [["Left", "Right", "Bottom"], ["Top", "Bottom"]],
    //                 Container: $diagram
    //             });
    //             alert(22);
    //             _.each(links, function (link) {
    //                 plumb.connect({
    //                     source: link.from,
    //                     target: link.to,
    //                     connector: ["Flowchart",
    //                         {
    //                             cornerRadius: 3,
    //                             stub: 16
    //                         }
    //                     ],
    //                     endpoints: ["Blank", "Blank"],
    //                     overlays: [["Arrow", {location: 1, width: 10, length: 10}]],
    //                 });
    //             });
    //             var dg = new dagre.graphlib.Graph();
    //             dg.setGraph({nodesep: 30, ranksep: 30, marginx: 50, marginy: 50});
    //             dg.setDefaultEdgeLabel(function () {
    //                 return {};
    //             });
    //             $container.find(".item").each(
    //                 function (idx, node) {
    //                     var $n = $(node);
    //                     var box = {
    //                         width: Math.round($n.outerWidth()),
    //                         height: Math.round($n.outerHeight())
    //                     };
    //                     dg.setNode($n.attr('id'), box);
    //                 }
    //             );
    //             plumb.getAllConnections()
    //                 .forEach(function (edge) {
    //                     dg.setEdge(edge.source.id, edge.target.id);
    //                 });
    //             dagre.layout(dg);
    //             var graphInfo = dg.graph();
    //             dg.nodes().forEach(
    //                 function (n) {
    //                     var node = dg.node(n);
    //                     var top = Math.round(node.y - node.height / 2) + 'px';
    //                     var left = Math.round(node.x - node.width / 2) + 'px';
    //                     $('#' + n).css({left: left, top: top});
    //                 });
    //             plumb.repaintEverything();
    //             _.defer(function () {
    //                 $panzoom = $container.find('.panzoom').panzoom({
    //                     minScale: minScale,
    //                     maxScale: maxScale,
    //                     increment: incScale,
    //                     disablePan: false,
    //                     disableZoom: false,
    //                     cursor: "",
    //                     ignoreChildrensEvents: true
    //                 }).on("panzoomstart", function (e, pz, ev) {
    //                         $panzoom.css("cursor", "move");
    //                     })
    //                     .on("panzoomend", function (e, pz) {
    //                         $panzoom.css("cursor", "");
    //                     });
    //                 $panzoom.parent()
    //                     .on('mousewheel.focal', function (e) {
    //                         if (e.ctrlKey || e.originalEvent.ctrlKey) {
    //                             e.preventDefault();
    //                             var delta = e.delta || e.originalEvent.wheelDelta;
    //                             var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
    //                             $panzoom.panzoom('zoom', zoomOut, {
    //                                 animate: true,
    //                                 exponential: false,
    //                             });
    //                         } else {
    //                             e.preventDefault();
    //                             var deltaY = e.deltaY || e.originalEvent.wheelDeltaY || (-e.originalEvent.deltaY);
    //                             var deltaX = e.deltaX || e.originalEvent.wheelDeltaX || (-e.originalEvent.deltaX);
    //                             $panzoom.panzoom("pan", deltaX / 2, deltaY / 2, {
    //                                 animate: true,
    //                                 relative: true,
    //                             });
    //                         }
    //                     })
    //                     .on("mousedown touchstart", function (ev) {
    //                         var matrix = $container.find(".panzoom").panzoom("getMatrix");
    //                         var offsetX = matrix[4];
    //                         var offsetY = matrix[5];
    //                         var dragstart = {x: ev.pageX, y: ev.pageY, dx: offsetX, dy: offsetY};
    //                         $(ev.target).css("cursor", "move");
    //                         $(this).data('dragstart', dragstart);
    //                     })
    //                     .on("mousemove touchmove", function (ev) {
    //                         var dragstart = $(this).data('dragstart');
    //                         if (dragstart) {
    //                             var deltaX = dragstart.x - ev.pageX;
    //                             var deltaY = dragstart.y - ev.pageY;
    //                             var matrix = $container.find(".panzoom").panzoom("getMatrix");
    //                             matrix[4] = parseInt(dragstart.dx) - deltaX;
    //                             matrix[5] = parseInt(dragstart.dy) - deltaY;
    //                             $container.find(".panzoom").panzoom("setMatrix", matrix);
    //                         }
    //                     })
    //                     .on("mouseup touchend touchcancel", function (ev) {
    //                         $(this).data('dragstart', null);
    //                         $(ev.target).css("cursor", "");
    //                     });
    //             });
    //             var currentScale = 1;
    //             $container.find(".diagram .item").draggable({
    //                 start: function (e) {
    //                     var pz = $container.find(".panzoom");
    //                     currentScale = pz.panzoom("getMatrix")[0];
    //                     $(this).css("cursor", "move");
    //                     pz.panzoom("disable");
    //                 },
    //                 drag: function (e, ui) {
    //                     ui.position.left = ui.position.left / currentScale;
    //                     ui.position.top = ui.position.top / currentScale;
    //                     if ($(this).hasClass("jsplumb-connected")) {
    //                         plumb.repaint($(this).attr('id'), ui.position);
    //                     }
    //                 },
    //                 stop: function (e, ui) {
    //                     var nodeId = $(this).attr('id');
    //                     if ($(this).hasClass("jsplumb-connected")) {
    //                         plumb.repaint(nodeId, ui.position);
    //                     }
    //                     $(this).css("cursor", "");
    //                     $container.find(".panzoom").panzoom("enable");
    //                 }
    //             });
    //
    //             var clickGapTime = null;
    //
    //             //双击
    //             $container.find(".diagram .item").dblclick(function (e) {
    //                 // console.log(e.currentTarget);
    //                 clearTimeout(clickGapTime);
    //                 //真正双击代码
    //                 console.log("dbclick");
    //                 StreamDiagramEditor.ondblclickNode(e.currentTarget);
    //             });
    //             //点击
    //             $(".item").on('click', function (e) {
    //                 // console.log(e.currentTarget);
    //                 clearTimeout(clickGapTime);
    //                 clickGapTime = setTimeout(function(){
    //                     console.log("click");
    //                     //单击事件在这里
    //                     StreamDiagramEditor.onclickNode(e.currentTarget);
    //                 }, 300);
    //             });
    //             return plumb;
    //         });
    //     },
    //
    //     onclickNode: function(item) {
    //         console.log(item);
    //     },
    //
    //     ondblclickNode: function(item) {
    //         console.log(item);
    //     },
    //
    //     onclickLink: function(link) {
    //
    //     },
    //
    //     updateLinks: function (links) {
    //         alert(11);
    //         console.log(plumb);
    //     }
    // }
}).call(typeof window !== 'undefined' ? window : this);
