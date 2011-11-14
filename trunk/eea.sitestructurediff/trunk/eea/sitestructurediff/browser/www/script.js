(function($) {
$(function () {
  Panel = {};

  // jsTree setup
  Panel.jsTree = $.tree_create();
  Panel.jsTree.init($("#tree-panel .tree"),
    { data : { type : "json",
      async : true,
        url : "@@sitemap-data",
      async_data : function (NODE) {
        return {
          path : $(NODE).attr("path") || 0
        };
      }
    },
  rules : { draggable : "all", multiple : "ctrl" },
    callback : {
      onopen : function (n) {
        if(n.id) {
          nId = "#" + n.id.replace("-0","-1");
        StatusPanel.jsTree.open_branch($(nId));
        }
        },
      onclose : function (n) {
        if(n.id) {
          nId = "#" + n.id.replace("-0","-1");
        StatusPanel.jsTree.close_branch($(nId));
        }
      }
    },
      ui : {
    context : [{ id : "sync",
      label : "Sync translations",
      icon : "",
      visible : function (NODE, TREE_OBJ) {  return true;   },
      action  : function (NODE, TREE_OBJ) {
        var path = $(NODE[0]).attr("path");
        if ( typeof(path) == 'undefined') {
            path = '0';
        }
            $.ajax({ method: "get",
          url: "@@sync-translation",
            data: "path="+path,
        complete: function(){ alert('complete');},
          success: function(){
            Panel.jsTree.refresh(NODE); }
          }); }
    },
      { id : "addTranslations",
    label : "Sync structure",
    icon : "",
    visible : function (NODE, TREE_OBJ) {  return true;   },
    action  : function (NODE, TREE_OBJ) {
    var path = $(NODE[0]).attr("path");
    if ( typeof(path) == 'undefined') {
        path = '0';
    }
        $.ajax({ method: "get",
      url: "@@sync-structure",
        data: "path="+path,
    complete: function(){ alert('complete');},
      success: function(){
        Panel.jsTree.refresh(NODE); }
      }); }
    } ] }
  });
  Panel.creating = 0;

  Panel.move = function(n,r,h) {};
  Panel.create = function () {
    Panel.jsTree.create(false, (Panel.jsTree.container.find("li").size() === 0 ? -1 : false) );
  };
  Panel.rename = function () { Panel.jsTree.rename(); };
  Panel.remove = function () { Panel.jsTree.remove(); };
  Panel.copy  = function () { if(Panel.jsTree.selected) { Panel.jsTree.copy(); } };
  Panel.cut  = function () { if(Panel.jsTree.selected) { Panel.jsTree.cut(); } };
  Panel.paste  = function () { Panel.jsTree.paste(); };

  // Interface hooks
  $("#tree-panel .menu")
    .find("a").not(".lang")
      .bind("click", function () {
        try { Panel[$(this).attr("rel")](); } catch(err) { }
        this.blur();
      })
    .end().end()
    .children(".cmenu")
    .hover( function () { $(this).addClass("hover"); }, function () { $(this).removeClass("hover"); });

  //Status panel init

  StatusPanel = {};

  // jsTree setup
  StatusPanel.jsTree = $.tree_create();
  StatusPanel.jsTree.init($("#status-panel"),
    { data : { type : "json",
      async : true,
        url : "@@status-data",
      async_data : function (NODE) {
        return { path : $(NODE).attr("path") || 0 };
      }
    },
  rules : { draggable : "all", multiple : "ctrl" },
    callback : {
      onopen : function (n) {
        if(n.id) {
          nId = "#" + n.id.replace("-1","-0");
        Panel.jsTree.open_branch($(nId));
        }
        },
      onclose : function (n) {
        if(n.id) {
          nId = "#" + n.id.replace("-1","-0");
        Panel.jsTree.close_branch($(nId));
        }
      }
    },
      ui : {
    context : [{ id : "sync",
      label : "Sync translations",
      icon : "",
      visible : function (NODE, TREE_OBJ) {  return true;   },
      action  : function (NODE, TREE_OBJ) {
        var path = $(NODE[0]).attr("path");
        if ( typeof(path) == 'undefined') {
            path = '0';
        }
            $.ajax({ method: "get",
          url: "@@sync-translation",
            data: "path="+path,
        complete: function(){ alert('complete');},
          success: function(){
            Panel.jsTree.refresh(NODE); }
          }); }
    },
      { id : "addTranslations",
    label : "Sync structure",
    icon : "",
    visible : function (NODE, TREE_OBJ) {  return true;   },
      action  : function (NODE, TREE_OBJ) {  alert('adding missing translations'); }
    } ] }
  });
  StatusPanel.creating = 0;

  StatusPanel.move = function(n,r,h) {
  };
  StatusPanel.create = function () {
    StatusPanel.jsTree.create(false, (StatusPanel.jsTree.container.find("li").size() === 0 ? -1 : false) );
  };
  StatusPanel.rename = function () { StatusPanel.jsTree.rename(); };
  StatusPanel.remove = function () { StatusPanel.jsTree.remove(); };
  StatusPanel.copy  = function () { if(StatusPanel.jsTree.selected) { StatusPanel.jsTree.copy(); } };
  StatusPanel.cut  = function () { if(StatusPanel.jsTree.selected) { StatusPanel.jsTree.cut(); } };
  StatusPanel.paste  = function () { StatusPanel.jsTree.paste(); };

});
})(jQuery);