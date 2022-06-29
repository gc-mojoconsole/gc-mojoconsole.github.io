qucick_command = [
    {name: "治疗全部角色", command: "heal", args: []},
    {name: "获取当前位置", command: "position", args: []},
    {name: "给予摩拉", command: "give 202", args: [
        {type: "number", default: 100000, width: 145, prepend: "x"}
    ]},
    {name: "开启/关闭无敌模式", command: "prop godmode", args: [
        {type: "checkbox", default: true, width: 145, label: "开启"}
    ]},
    {name: "无限体力模式", command: "prop nostamina", args: [
        {type: "checkbox", default: true, width: 145, label: "开启"}
    ]},
    {name: "无限元素能量模式", command: "prop ue", args: [
        {type: "checkbox", default: true, width: 145, label: "开启"}
    ]},
    {name: "给予原石", command: "give 201", args: [
        {type: "number", default: 10000, width: 120, prepend: "x"}
    ]},
    {name: "给予纠缠之缘", command: "give 223", args: [
        {type: "number", default: 10000, width: 100, prepend: "x"}
    ]},
    {name: "给予相遇之缘", command: "give 224", args: [
        {type: "number", default: 10000, width: 100, prepend: "x"}
    ]},
    {name: "设置世界等级(需要重新登陆)", command: "prop worldlevel", args: [
        {type: "number", default: 8, width: 60}
    ]}, 
    {name: "获取全部道具", command: "give all", args: []},
    {name: "清除全部道具", command: "clear all", args: []},
    {name: "设置当前角色E技能等级", command: "talent e", args: [
        {type: "number", default: 10, width: 60}
    ]},
    {name: "设置当前角色Q技能等级", command: "talent q", args: [
        {type: "number", default: 10, width: 60}

    ]},
    {name: "设置当前角色普攻等级", command: "talent n", args: [
        {type: "number", default: 10, width: 60}
    ]},
]

function genQuickCommand() {
    var i = 0;
    var arg = 0;
    for (i=0; i< qucick_command.length; i++) {
        var command = qucick_command[i];
        var div = document.createElement("div");
        var label = document.createElement("span");
        var div2 = document.createElement("div");
        var button = document.createElement("button");
        var hr = document.createElement("hr");
        var hiddenCommand = document.createElement("input");

        hr.classList.add("solid");
        div.classList.add('commandGroup');
        label.innerText = command.name;
        button.innerText = "Go!";
        div.appendChild(label);
        div.appendChild(div2);

        hiddenCommand.value = command.command;
        hiddenCommand.classList.add('hidden');
        div2.appendChild(hiddenCommand);
        for (arg = 0; arg < command.args.length; arg++){
            var arg_item = command.args[arg];
            switch (arg_item.type) {
                case "number": 
                    var input = document.createElement('input');
                    input.type = arg_item.type;
                    input.value = arg_item.default;
                    if (arg_item.prepend) input.setAttribute("prepend", arg_item.prepend);
                    if (arg_item.width) {
                        input.style.width = arg_item.width + 'px';
                    }
                    break;
                case "checkbox":
                    var input = document.createElement('label');
                    var checkbox = document.createElement('input');
                    checkbox.type = "checkbox";
                    checkbox.setAttribute("checked", arg_item.default);

                    if (arg_item.width) {
                        label.style.width = arg_item.width + 'px';
                    }
                    input.appendChild(checkbox);
                    input.innerHTML += `<span class="checkable">${arg_item.label}</span>`
                    break;
            }

            div2.appendChild(input);
        }


        div2.appendChild(button);
        panel.appendChild(div);
        button.onclick = (e) => {
            var parent = e.target.parentNode;
            var payload = "";
            var first = true;
            for(var child=parent.firstChild; child!==null; child=child.nextSibling) {
                if (child.tagName == "INPUT") {
                    if (!first) {
                        payload += " ";
                    }
                    first = false;
                    payload += (child.getAttribute("prepend") || "")  + child.value;
                }
                if (child.tagName == "LABEL") {
                    if (!first) {
                        payload += " ";
                    }
                    payload += child.firstChild.checked? "1": "0";
                }

            }
            sendCommand(payload);
        }
        panel.appendChild(hr);
    }
}