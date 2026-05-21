
let currentStep = 1;
// 步骤刷新
function refreshStep(){
    for(let i=1;i<=3;i++){
        document.getElementById("step"+i+"-tag").classList.remove("active");
        document.getElementById("step"+i).classList.remove("active");
    }
    document.getElementById("step"+currentStep+"-tag").classList.add("active");
    document.getElementById("step"+currentStep).classList.add("active");
}
function nextStep(){if(currentStep<3)currentStep++;refreshStep()}
function prevStep(){if(currentStep>1)currentStep--;refreshStep()}

// 禁用全部按钮
function setBtnStatus(status){
    let btns = document.querySelectorAll(".btn");
    btns.forEach(btn=>{btn.disabled = status})
}

async function startRun(){
    const f=document.getElementById("mainForm");
    const hosts = f.hosts.value.trim().split("\n").filter(x=>x.trim());
    if(hosts.length === 0){
        alert("请输入服务器IP列表！");
        return;
    }
    // 清空日志、锁定按钮防止重复提交
    document.getElementById("logs").innerHTML="";
    setBtnStatus(true);
    document.getElementById("bar").style.width="0%";

    // 动态生成日志面板
    hosts.forEach(h=>{
        const d=document.createElement("div");d.className="log";
        d.innerHTML=`<h4>🖥️ 服务器：${h}</h4><div id="L${h}"></div>`;
        document.getElementById("logs").appendChild(d);
    });

    let body = {
        hosts:hosts,
        port:parseInt(f.port.value),
        username:f.username.value,
        password:f.password.value,
        host_suffix:f.host_suffix.value,
        yum_repo:f.yum_repo.checked,ntp:f.ntp.checked,ntp_server:f.ntp_server.value,
        firewall:f.firewall.checked,ssh_optimize:f.ssh_optimize.checked,
        stop_services:f.stop_services.checked,numa_thp:f.numa_thp.checked,
        swap:f.swap.checked,limits:f.limits.checked,history:f.history.checked,
        kernel:f.kernel.checked,ipv6:f.ipv6.checked,tools:f.tools.checked,
        tools_list:f.tools_list.value,container:f.container.checked,
        java:f.java.checked,java_version:f.java_version.value,docker:f.docker.checked
    };
    const res = await fetch("/run",{
        method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)
    });
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let done=0,total=hosts.length;
    while(1){
        const {done:d,value}=await reader.read();
        if(d)break;
        dec.decode(value).split("\n").filter(x=>x.trim()).forEach(line=>{
            try{
                let obj = JSON.parse(line);
                if(obj.type==="log") {
                    let html = obj.data;
                    // 简单高亮
                    html = html.replace(/✅/g,'<span style="color:#00B42A">✅</span>');
                    html = html.replace(/❌/g,'<span style="color:#F53F3F">❌</span>');
                    html = html.replace(/OUT:/g,'<span style="color:#94F5A5">OUT:</span>');
                    html = html.replace(/ERR:/g,'<span style="color:#FF7D00">ERR:</span>');
                    document.getElementById("L"+obj.host).innerHTML += html+"<br/>";
                }
                if(obj.type==="result"){
                    done++;
                    document.getElementById("bar").style.width = (done/total*100)+"%";
                }
            }catch(e){}
        });
    }
    setBtnStatus(false);
    alert("✅ 全部执行完成！");
}
