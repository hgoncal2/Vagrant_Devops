datacenter = "lab7"
data_dir = "/opt/consul"
node_name= "master"
client_addr="0.0.0.0"
enable_syslog= true
ui_config  {
        enabled=true
}

server = true
bind_addr = "worker"
bootstrap_expect=1
