from pyzabbix import ZabbixSender, ZabbixMetric

def send_zabbix_script_monitoring(status_code, config_options):
    metrics = []
    m = ZabbixMetric(config_options['APP']['SERVER_NAME'], config_options["APP"]["ZABBIX_METRIC"], status_code)
    metrics.append(m)
    zbx = ZabbixSender(use_config=config_options['APP']['ZABBIX_CONFIG_FILE'])
    zbx.send(metrics)