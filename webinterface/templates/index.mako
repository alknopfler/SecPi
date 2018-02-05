<%inherit file="main.mako"/>

<%def name="active_tab()"><% return "home" %></%def>

<h1>Welcome to AlkAlarm</h1>


<div ng-controller="ActivateController as actCtrl">
        <div ng-show="actCtrl.active_setups.length == 0" >
        <p style="color:#FF5533; font-weight:bold;">Alarma APAGADA:
                <p ng-model="actCtrl.activate_setup=actCtrl.inactive_setups[0]" ></p>
                <input type="button" ng-click="actCtrl.activate()" class="btn btn-success" value="ACTIVAR" />
        </div>
        <div ng-show="actCtrl.active_setups.length > 0">
        <p style="color:#048806; font-weight:bold;"> Alarma ENCENDIDA:
                <p ng-model="actCtrl.deactivate_setup=actCtrl.active_setups[0]" ></p>
                <input style="color:#FF5533;" type="button" ng-click="actCtrl.deactivate()" class="btn btn-success" value="DESACTIVAR" />
        </div>
</div>

<div id="alarm_div">
	<h2>Alarms</h2>
	<div ng-controller="AckController as alarmCtrl" ackclass="alarm" sort="alarmtime desc">
		<input type="button" value="stop refresh" class="btn btn-success" id="refresh_toggle_alarm" name="refresh_toggle_alarm" ng-click="alarmCtrl.toggleRefresh()" />
		<input type="button" value="acknowledge all" class="btn btn-success" id="ack_alarm" name="ack_alarm" ng-click="alarmCtrl.ackAll()" />
		<div class="alarm_entry" ng-repeat="alarm in alarmCtrl.entries" ng-show="alarm.message != null">
			<b>{{alarm.alarmtime | date:'dd. MMM. yyyy, HH:mm:ss'}} <i>{{alarm.sensor_id}}:</i></b> {{alarm.message}}
			<span class="alarm_ack"><img src="/static/img/icons/ack.png" title="acknowledge" ng-click="alarmCtrl.ack($index)" /></span>
		</div>
	</div>
</div>

<div id="log_div">
	<h2>Log Messages</h2>
	<div ng-controller="AckController as logCtrl" ackclass="log" sort="logtime desc">
		<input type="button" value="stop refresh" class="btn btn-success" id="refresh_toggle_log" name="refresh_toggle_log" ng-click="logCtrl.toggleRefresh()" />
		<input type="button" value="acknowledge all" class="btn btn-success" id="ack_log" name="ack_log" ng-click="logCtrl.ackAll()" />
		<div class="log_entry" ng-repeat="log in logCtrl.entries" ng-show="log.message != null" ng-class="'lvl'+log.level">
			<b>{{log.logtime | date:'dd. MMM. yyyy, HH:mm:ss'}} <i>{{log.sender}}:</i></b> {{log.message}}
			<span class="log_ack"><img src="/static/img/icons/ack.png" title="acknowledge" ng-click="logCtrl.ack($index)" /></span>
		</div>
	</div>
</div>

<span class="clear"></span>
