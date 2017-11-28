function showExecutions(workflowId, workflowName) {
	if ($("#collapse"+workflowName).hasClass('in')) {
		return;
	}
	ajaxDo('/cronjobs/api/workflow/executions', 'GET', {'id': workflowId}, function(data) {
		$("#data"+workflowName).html('');
		$(data).each(function(i, job){
			var item = '<div href="#" class="list-group-item">'
				+ job.run_time + '&nbsp;&nbsp;';
			if (job.status == 'Executed') {
				item += '<font color="green">' + job.status + '</font>&nbsp;'
					+ '<pre>' + job.retval + '</pre>';
			} else {
				if (job.status == 'Error!') {
					item += '<font color="red">' + job.status + '</font>&nbsp;';
				} else {
					item += '<font color="red">' + job.status + '</font>&nbsp;';
				}
				item += job.exception
					+ '<pre>' + job.traceback + '</pre>';
			}
			item += '</div>';
			$("#data"+workflowName).append(item);
		});
	});
}

function showCreateWorkflow() {
	$('#workflowId').attr('value', '');
	$('#workflowName').attr('value', '');
	$('#workflowModal').modal('show');
}

function showWorkflow(id) {
	ajaxDo('/cronjobs/api/workflow/get/'+id, 'GET', {}, function(response) {
		$('#workflowId').attr('value', response.id);
		$('#workflowName').attr('value', response.name);
		$('#workflow').flowchart('setData', JSON.parse(response.data));
	});
}

function addWorkflowMenu(id, name) {
	if ($('#workflowMenu'+id).length != 0){
		return;
	}
	var menu = '<li id="workflowMenu' + id + '"><a href="#" onclick="showWorkflow(\'' +id+'\')">'
		+name+'</a></li>';
	$('#workflowList').append(menu);
}

function loadWorkflowlist() {
	ajaxDo('/cronjobs/api/workflow/list', 'GET', {}, function(data) {
		$.each(data, function(index, item) {
			addWorkflowMenu(item.id, item.name);
		});
	});
}

function createWorkflow() {
	var data = {
		operators: {
			operator: {
				top: 20,
				left: 20,
				properties: {
					title: 'Schedule',
					inputs: {
						input_1: {
							label: '18:00 every day',
						}
					},
					outputs: {
						output_1: {
							label: 'time'
						}
					},
					params: {
						param1: 'Hello'
					},
				}
			}
		}
	};
	$('#workflow').flowchart('setData', data);
	$('#workflowId').attr('value', '');
	saveWorkflow();
}

function saveWorkflow() {
	ajaxDo('/cronjobs/api/workflow/update', 'POST', {
		id: $('#workflowId').val(),
		name: $('#workflowName').val(),
		data: JSON.stringify($('#workflow').flowchart('getData'))
	}, function(data) {
		$('#workflowModal').modal('hide');
		addWorkflowMenu(data.id, data.name);
		$('#workflowId').attr('value', data.id);
		$('#workflowName').attr('value', data.name);
	});
}

function runWorkflow() {
	ajaxDo('/cronjobs/api/workflow/run/'+$('#workflowId').val(), 'GET', {
	}, function(response){
		alert(response);
	});
}

function deleteWorkflow() {
	ajaxDo('/cronjobs/api/workflow/delete/'+$('#workflowId').val(), 'GET', {
	}, function(response) {
		$('#workflowMenu'+response.id).remove();
		$('#workflow').flowchart('setData', {});
	});
}

function pauseWorkflow() {
	ajaxDo('/cronjobs/api/workflow/pause/'+$('#workflowId').val(), 'GET', {
	}, function(data) {
		alert(data);
	});
}

function resumeWorkflow() {
	ajaxDo('/cronjobs/api/workflow/resume/'+$('#workflowId').val(), 'GET', {
	}, function(data) {
		console.log(data);
	});
}

$(document).ready(function(){
	$('#workflow').flowchart({data: {}});
	$('#createWorkflowBtn').click(function(){
		createWorkflow();
	});
	$('#saveWorkflowBtn').click(function(){
		saveWorkflow();
	});
	$('#deleteWorkflowBtn').click(function(){
		deleteWorkflow();
	});
	$('#runWorkflowBtn').click(function(){
		runWorkflow();
	});
	$('#pauseWorkflowBtn').click(function(){
		pauseWorkflow();
	});
	$('#resumeWorkflowBtn').click(function(){
		resumeWorkflowBtn();
	});

	loadWorkflowlist();

	$('#deleteStepBtn').click(function() {
		$('#workflow').flowchart('deleteSelected');
	});
	$('#addStepBtn').on('click', function() {
		$('#addStepDiv').modal('show');
	});
	$('#saveStepBtn').on('click', function() {
		var stepId = $.now();
		var stepData = {
			top: 60,
			left: 500,
			properties: {
				title: $('#stepId').val(),
				inputs: {
					input_1: {
						label: $('#stepInput').val()
					}
				},
				outputs: {
					output_1: {
						label: $('#stepOutput').val()
					}
				}
			}
		};
		$('#workflow').flowchart('createOperator', stepId, stepData);
	});
});
