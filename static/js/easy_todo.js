$("#todo_list_dd").on("change", function() {
  console.log("on change");
  window.location.href = window.location.pathname + "?todolist_id_filter="+$("#todo_list_dd").val()
});

$(".hide-alert-on-click").on("click", function() {
  $(this).parent().parent().hide();
});

$(document).ready(function () {
  target_datepicker = $('#target_datepicker').datepicker({
    language: "es",
    autoclose: true,
    format: "dd/mm/yyyy",
    todayHighlight: true,
    startDate: new Date(),
  });
  target_datepicker.on('hide', function(e) {
    e.stopPropagation();
  });
  target_datepicker.datepicker('setDate', 'today');
  $("#selected_todolist_title").text($("#todo_list_dd option:selected").text());
});
$("#delete_todolist_btn").on("click", function() {
  if(!confirm("Delete List, Are you sure?")) {
    return;
  }
  $.ajax({
    type: "POST",
    url: "/todo_lists/manage",
    data: {"todo_list_id": $("#todo_list_dd").val()},
    beforeSend: function (xhr){
      xhr.setRequestHeader('X-CSRFToken', $("[name=csrfmiddlewaretoken]").val());
    },
    error: function(error) {},
    success: function(resp) {
      location.href = "/easy_todo";
    }
  });
});

$('#TodoListCreateModal').on('show.bs.modal', function (event) {
  var modal = $(this)
  modal.find('#todo_list_title').val('');
});

$('#TodoItemCreateModal').on('show.bs.modal', function (event) {
  var modal = $(this)
  $("#create_task_success_msg").hide();
  $("#create_task_error_msg").hide();
});

$('#TodoItemCreateModal').on('hide.bs.modal', function (event) {
  location.reload()
});


$("#create_todolist_btn").click(function() {
  $.ajax({
    type: "POST",
    url: "/todo_lists/create",
    data: {"todo_list_name": $("#todo_list_name_input").val()},
    beforeSend: function (xhr){
      xhr.setRequestHeader('X-CSRFToken', $("[name=csrfmiddlewaretoken]").val());
    },
    error: function(error) {console.log(error);},
    success: function(resp) {
      if (!resp["error"]) {
        alert("List already exists")
      }
      window.location.href = window.location.pathname + "?todolist_id_filter="+resp["id"]
    }
  });
});

$("#create_todoitem_btn").click(function() {
  if ($("#todo_item_desc_input").val() === "") {
    $("#create_task_success_msg").hide();
    $("#create_task_error_msg").find("strong").text("Hiss!!! please enter task description first");
    $("#create_task_error_msg").show();
    return;
  }
  $.ajax({
    type: "POST",
    url: "/todo_items/create",
    data: {"todo_desc": $("#todo_item_desc_input").val(), "todo_list_id": $("#todo_list_dd").val(), "todo_target_date": $("#todo_target_date").val()},
    beforeSend: function (xhr){
      xhr.setRequestHeader('X-CSRFToken', $("[name=csrfmiddlewaretoken]").val());
    },
    error: function(resp) {
      resp = JSON.parse(resp.responseText);
      $("#create_task_success_msg").hide();
      $("#create_task_error_msg").find("strong").text(resp["msg"]);
      $("#create_task_error_msg").show();
    },
    success: function(resp) {
      $("#create_task_error_msg").hide();
      $("#create_task_success_msg").find("strong").text(resp["msg"]);
      $("#create_task_success_msg").show();
    }
  });
});

function manage_todo_item(op, todo_item_id) {
  $.ajax({
    type: "POST",
    url: "/todo_items/manage",
    data: {todo_item_id: todo_item_id, op: op},
    beforeSend: function (xhr){
      xhr.setRequestHeader('X-CSRFToken', $("[name=csrfmiddlewaretoken]").val());
    },
    error: function(error) {console.log(error);},
    success: function() {
      location.reload();
    }
  });
}

function edit_todo_item(todo_list_id, todo_item_id) {
	$("#edit_todo_item_id").val(todo_item_id);
	$("#edit_todo_list_dd").val(todo_list_id);
	$("#edit_todo_item_id_label").text("# " + todo_item_id);
	$("#edit_todo_item_desc_input").val($("#item_" + todo_item_id + "_desc").text());

	edit_target_datepicker = $('#edit_target_datepicker').datepicker({
    language: "es",
    autoclose: true,
    format: "dd/mm/yyyy",
    todayHighlight: true,
    startDate: new Date(),
  });
  edit_target_datepicker.on('hide', function(e) {
    e.stopPropagation();
  });
	tokens = $("#item_" + todo_item_id + "_target_date").text().split("/");
	edit_target_date = new Date(parseInt(tokens[2]), parseInt(tokens[1])-1, parseInt(tokens[0]))
  edit_target_datepicker.datepicker('setDate', edit_target_date);
  $("#TodoItemEditModal").modal("show");
}

$("#save_todoitem_changes_btn").click(function() {
  data = {
      "todo_item_id": parseInt($("#edit_todo_item_id").val()),
      "desc": $("#edit_todo_item_desc_input").val(),
      "todo_list_id": parseInt($("#edit_todo_list_dd").val()),
      "target_date": $("#edit_todo_target_date").val(),
    };
  $.ajax({
    type: "PATCH",
    url: "/todo_items/manage",
    data: data,
    beforeSend: function (xhr){
      xhr.setRequestHeader('X-CSRFToken', $("[name=csrfmiddlewaretoken]").val());
    },
    error: function(error) {
      console.log(error);
    },
    success: function(resp) {
      if (resp["error"] == true) {
        show_msg(resp["error"], resp["msg"], "#edit_task_msg")
      } else {
        location.reload()
      }
    }
  });
});

function show_msg(error, msg, root) {
  if (error == true) {
    html = '<div class="alert alert-danger mt-3" role="alert">' + msg + '</div>'
  } else {
		html = '<div class="alert alert-success mt-3" role="alert">' + msg + '</div>'
  }
  $(root).html(html);
}

$("#rename_todolist_btn").click(function() {
  $.ajax({
    type: "PATCH",
    url: "/todo_lists/manage",
    data: {todo_list_id: $("#todo_list_dd").val(), new_title: $("#todo_list_newtitle_input").val()},
    beforeSend: function (xhr){
      xhr.setRequestHeader('X-CSRFToken', $("[name=csrfmiddlewaretoken]").val());
    },
    error: function(error) {console.log(error);},
    success: function(resp) {
      if (resp["error"] == true) {
        show_msg(resp["error"], resp["msg"], "#todolist_rename_msg");
      } else {
        location.reload();
      }
    }
  });
})

function update_location_href(param_key, param_value) {
  params = {}
  tokens = location.href.split("?")
  if (tokens.length > 1) {
    tokens[1].split("&").forEach((token) => {
      params[token.split("=")[0]] = token.split("=")[1];
    })
  }
  params[param_key] = param_value;
  new_href = "?";
  Object.keys(params).forEach((key) => {
    if (new_href.length > 1) {
      new_href += "&";
    }
    new_href += key +"="+ params[key]
  });
  window.location.href = window.location.pathname + new_href
}

$("input[name=todo_item_status_filter]").change(function() {
  update_location_href("todo_item_status_filter", $(this).attr("data-value"));
});

$("#todolist_rename_modal_open_btn").click(function() {
	if ($("#todo_list_dd").val() == "-1") {
		alert("Please select a Todo list first to rename");
	} else {
		$("#TodoListRenameModal").modal("show");
	}
})
