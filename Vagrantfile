# -*- mode: ruby -*-
# vi: set ft=ruby :
#Definições de variáveis

IP_NW="192.168.10."
IP_START=2
NUM_WORKER=5
#port=2523
#------------------------------------------------------------------------#
Vagrant.configure("2") do |config|
  
  config.vm.synced_folder ".", "/vagrant", disabled: true
 # config.vm.network "forwarded_port", guest: 8500, host: 8500
  config.vm.synced_folder "shared_1/", "/etc/shared"
   






  config.vm.provision "shell", env: {"IP_NW" => IP_NW, "IP_START" => IP_START}, inline: <<-SHELL #abre shell
      apt-get update -y #corre comando para dar update às packages
      echo "$IP_NW$((IP_START)) master" >> /etc/hosts #adiciona hostname do master ao ficheiro de hosts
      echo "$IP_NW$((IP_START)) master" > /etc/shared/ip_v.txt #Linha necessária para o script local curlv
      
      #Faz download do consul
      wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
      echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
      sudo apt update && sudo apt install consul #instala o consul
  SHELL
  
config.vm.provision :docker do |d| # Usa a provision de docker para facilitar instalação e configurações desta
        d.post_install_provision "shell" , inline:" sudo systemctl enable docker.service; sudo systemctl enable containerd.service;" #Inicia docker em boot
  end
  
  (1..NUM_WORKER).each do |i|
  config.vm.provision "shell", env: {"IP_NW" => IP_NW, "IP_START" => IP_START}, inline: <<-SHELL #abre shell
        echo "$IP_NW$((IP_START+#{i})) worker#{i}" >> /etc/hosts #adiciona hostname dos workers ao ficheiro de hosts
        echo "$IP_NW$((IP_START+#{i})) worker#{i}" >> /etc/shared/ip_v.txt #Linha necessária para o script local curlv
    SHELL
  end

  
  config.vm.box = "bento/ubuntu-20.04" #define imagem a ser usada
 
  config.vm.box_check_update = true #verifica se existem novos updates à imagem

  config.vm.provider "virtualbox" do |vb| #especifica virtualbox como provider
        vb.memory = "512" #define a memória base da VM
        vb.cpus = "1" #define número de CPUs da VM
        vb.customize ["modifyvm", :id, "--nataliasmode1", "proxyonly"]
    end
	
 config.vm.define "master" do |master| #criação da VM master
    master.vm.hostname="master" #define hostname da VM
    master.vm.network "private_network", ip: IP_NW + "#{IP_START}" # Define para usar private network e configura endereço IP
    master.vm.provision "shell", env: {"IP_NW" => IP_NW, "IP_START" => IP_START}, inline: <<-SHELL
        rm -f /etc/consul.d/consul.hcl #remove ficheiro de configuração do consul se já existir
        cp  /etc/shared/consul_m.hcl /etc/consul.d/consul.hcl #copia ficheiro de configuração do consul da pasta partilhada para diretoria local(na VM)
        sed -i "s/worker/$IP_NW$((IP_START))/g" /etc/consul.d/consul.hcl  #substitui a palavra chave "worker" pelo IP da VM
        sudo systemctl enable consul #inicia consul em boot
        sudo systemctl start consul #inicia o processo consul
        apt install nginx -y #instala nginx
        rm -f /etc/consul.d/config_consul_templt/consul-template-config.hcl && mkdir /etc/consul.d/config_consul_templt/ #remove ficheiro de configuração de consul template se já existir
        cp /etc/shared/consul/consul-template-config.hcl /etc/consul.d/config_consul_templt/consul-template-config.hcl #copia ficheiro de configuração do consul template da pasta partilhada para a diretoria local(na VM)
        rm -f /etc/nginx/conf.d/load-balancer.conf.ctmpl #remove o ficheiro de configuração nginx/consul-template se já existir
        cp /etc/shared/consul/load-balancer.conf.ctmpl /etc/nginx/conf.d/load-balancer.conf.ctmpl #copia ficheiro de configuração do nginx/consul-template da pasta partilhada para a diretoria local(na VM)
        rm -f /etc/nginx/sites-enabled/default #remove ficheiro default de sites disponíveis do nginx
        service nginx reload #dá reload ao serviço nginx para refletir a remoção do ficheiro na linha anterior
        cd /etc/consul.d #move para a diretoria 
        apt install unzip -y #é preciso instalar o unzip porque o ficheiro pré compilado do consul template vem em formato zip
        curl -O https://releases.hashicorp.com/consul-template/0.32.0/consul-template_0.32.0_linux_386.zip # faz download do ficheiro pré compilado do consul template
        unzip consul-template_0.32.0_linux_386.zip #dá unzip ao ficheiro
        rm -f /etc/systemd/system/consul_templt.service #remove serviço consul template se já existir
        cp /etc/shared/consul/consul_templt.service /etc/systemd/system/consul_templt.service #copia serviço consul template da pasta partilhada para o host(VM)
        chmod -x /etc/systemd/system/consul_templt.service
        systemctl enable consul_templt #inicia serviço/daemon consul template em boot
        systemctl start consul_templt # incia serviço/daemon consul_templt


    SHELL
   
end
(1..NUM_WORKER).each do |i| # ciclo for para criar cada VM worker

  config.vm.define "worker#{i}" do |worker|
    worker.vm.hostname = "worker#{i}" # define hostname da VM
    worker.vm.network "private_network", ip: IP_NW + "#{IP_START+i}" # Define para usar private network e configura endereço IP
    worker.vm.provision "shell", env: {"IP_NW" => IP_NW, "IP_START" => IP_START}, inline: <<-SHELL #abre shell
        rm -f /etc/consul.d/consul.hcl #remove ficheiro de configuração do consul,se houver
        cp  /etc/shared/consul_w.hcl /etc/consul.d/consul.hcl #copia ficheiro de configuração da pasta partilhada para host(VM)
        sed -i "s/wname/worker#{i}/g" /etc/consul.d/consul.hcl #substitui no ficheiro de configuração do consul a palavra chave "wname" pelo hostname da VM(para o nome do nó)
        sed -i "s/wj/$IP_NW$((IP_START))/g" /etc/consul.d/consul.hcl #substitui no ficheiro de configuração do consul a palavra chave "wj" pelo endereço IP do master(para o retry join)
        sed -i "s/wbind/$IP_NW$((IP_START+#{i}))/g" /etc/consul.d/consul.hcl #substitui no ficheiro de configuração do consul a palavra chave "wname" pelo IP da VM(para o bind_addr)
        rm -f /etc/consul.d/web-service.json #remove ficheiro de configuração de um serviço web no consul,se já houver
        cp /etc/shared/consul/web-service.json /etc/consul.d/web-service.json #copia da pasta partilhada para o host(VM)
        sudo systemctl enable consul #inicia consul em boot
        sudo systemctl start consul #inicia processo consul
        #consul reload 
        cp -r /etc/shared/consul_docker_web/web0/ ~/web#{i}/
        cd ~/web#{i}
        sed -i 's/one/#{i}/g' Website1/Website1.py
        docker network create --driver=bridge --subnet=192.190.0.0/24 br0
        rm -f /etc/systemd/system/docker_web.service
        cp /etc/shared/docker_web.service /etc/systemd/system/docker_web.service
        sed -i 's/one/web#{i}/g' /etc/systemd/system/docker_web.service
        chmod -x /etc/systemd/system/docker_web.service
        systemctl enable docker_web
        systemctl start docker_web

  
  SHELL

  
  end
  
    
  end

 
  end


