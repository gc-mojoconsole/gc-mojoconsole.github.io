
var delayedSearch = null;
function genQuest() {
    var panel = document.getElementById("panel");
    panel.innerHTML = `<div class="form">
    <h2>生成任务</h2>
    <div style="border: 1px solid gray; border-radius: 5px; padding: 1em;">
            <label for="quest-search">任务列表:</label>
                <div style="display: flex; flex-direction: column;">
                    <div style="display: flex; align-items: center; overflow: hidden;">
                        <input id="quest-search" style="flex: 4" type="text" placeholder="搜索任务名称" />
                        <button id="clear" style="margin-left: 0.25em; transition: all ease-in-out 0.5s; flex: 0; opacity: 0;">清除</button>
                    </div>
                    <div>
                        <input id="check-hidden" type="checkbox" name="HIDDEN" onchange="updateQuestList()" />
                        <label class="checkable" for="check-hidden">显示HIDDEN</label>
                        <input id="check-test" type="checkbox" name="test" onchange="updateQuestList()" />
                        <label class="checkable" for="check-test">显示(test)</label>
                        <input id="check-unrelease" type="checkbox" name="test" onchange="updateQuestList()" />
                        <label class="checkable" for="check-unrelease">显示UNRELEASE</label>
                    </div>
                    <div id="name-list" style="overflow-y: auto; overflow-x: hidden; max-height: 10em;height: 100%; transition: all ease-in-out 0.5s; display: flex; flex-wrap: wrap; ">
                    </div>
                </div>
    </div>
            <div style="border: 1px solid gray; border-radius: 5px; margin-top: 1em; padding: 1em; " >
                <label for="step-list" >进度选择:</label>
                <div id="step-list" style="margin-top: 2em; overflow-y: auto; overflow-x: hidden; max-height: 10em;justify-content: space-between; transition: all ease-in-out 0.5s; display: flex; flex-direction: column; ">
                </div>
            </div>
            <input type="hidden" id="quest-name" />
    </div>`;
    updateQuestList();

    document.getElementById("quest-search").oninput = (e) => {
        if (e.target.value.length > 0) {
            document.getElementById("clear").style.flex = 1;
            document.getElementById("clear").style.opacity = 1;
        } else {
            document.getElementById("clear").style.flex = 0;
            document.getElementById("clear").style.opacity = 0;
        }
        if (delayedSearch) {
            clearTimeout(delayedSearch);
        }
        delayedSearch = setTimeout(() => updateQuestList(), 500);
        document.getElementById("name-list").style.height = "10em";
    };
    document.getElementById("clear").onclick = ()=>{
        document.getElementById("quest-search").value = "";
        document.getElementById("step-list").innerHTML = "";
        updateQuestList();
    }
    document.getElementById("quest-search").onkeydown = (e) => {
        if(e.key == "Escape") {
            document.getElementById("quest-search").value = "";
            updateQuestList();
        }
    }
    document.getElementById("quest-name").setvalue = (v) => {
        document.getElementById("quest-name").value = v;
    }
    document.getElementById("name-list").onclick = (e) => {
        if (e.target.tagName == "INPUT") {
            var list = document.getElementById("name-list");
            list.style.height = "3em";
            var name = e.target.attributes['quest-name'].nodeValue ? e.target.attributes['quest-name'].nodeValue : "UNKNOWN";
            
            var content = `<div><input name="stack" type="radio" name="item-id" quest-name="${e.target.attributes['quest-name'].nodeValue}"">
                <span class="button">
                ${name}
                </span></div>`;
            list.innerHTML = content;
            document.getElementById("quest-search").value = name;
            document.getElementById("clear").style.flex = 1;
            document.getElementById("clear").style.opacity = 1;
            document.getElementById("quest-name").setvalue(e.target.attributes['quest-name'].nodeValue);
            updateSubQuestList();
        }
    }

    document.getElementById("step-list").onclick = (e) => {
        if (e.target.tagName == "BUTTON") {
            var option = () => {
                if (e.target.classList.contains("success")) {
                    return "add";
                } else {
                    return "finish";
                }
            };
            var quest_id = e.target.attributes['quest-id'].nodeValue;
            sendCommand(`quest ${option()} ${quest_id}`);
        }
    }

}

function updateQuestList() {
    var filter = document.getElementById("quest-search").value;
    var list = document.getElementById("name-list");
    var check_hidden = document.getElementById("check-hidden").checked;
    var check_test = document.getElementById("check-test").checked;
    var check_unrelease = document.getElementById("check-unrelease").checked;

    list.innerHTML = "";
    list.style.height = "10em";
    Object.entries(quest_list).forEach(element => {
        var quest_name = element[0];
        var quest_ids = element[1];
        if (filter == "" || quest_name.toLowerCase().indexOf(filter.toLowerCase()) != -1) {
            if (!check_hidden && quest_name.toLowerCase().indexOf("$hidden") != -1) {
                return;
            }
            if (!check_test && quest_name.toLowerCase().indexOf("(test)")  != -1 ){
                return;
            }
            if (!check_unrelease && quest_name.toLowerCase().indexOf("$unrelease") != -1) {
                return;
            }
            var o = document.createElement("label");
            o.style.marginLeft = "0.1em";
            var content = `<div style="display: flex;"><input name="stack" type="radio" name="quest-option" quest-name="${quest_name}" quest-step="${quest_ids.length}">
                <span class="button">
                    ${quest_name}
                </span><div style="margin-left:0.1em">&#128681; ${quest_ids.length}</div><div>`;
            o.innerHTML = content;
            list.appendChild(o);
        }

    });

}

function updateSubQuestList(){
    var quest_name = document.getElementById("quest-name").value;
    var step_list = document.getElementById("step-list");
    var total = quest_list[quest_name].length;
    var current = 0;
    step_list.innerHTML = "";
    quest_list[quest_name].forEach(id_desc => {
        current += 1;
        var o = document.createElement("div");
        o.style.display = "flex";
        o.style.alignItems = "center";
        o.style.justifyContent = "space-between";
        o.style.marginRight = "1em";
        o.style.marginTop = "0.4em";
        o.style.borderLeft = "0.3em solid green";
        o.style.borderRadius = "6px";
        o.style.background = "linear-gradient(90deg, rgba(215 252 252) 0%, rgba(173,254,255,0.390095413165266) 85%, rgba(173,254,255,0.0) 100%)";
        o.style.paddingRight = "0.3em";
        var id = id_desc[0];
        var desc = id_desc[1] ? id_desc[1] : "缺少描述";
        var content = `
            <div style="padding-left: 0.2em;">
                <div style="color: green;">${quest_name} 节点: ${current}/${total}</div>
                <div style="margin-left: 1em; font-style: italic;font-size: 0.8em;">${desc}</div>
            </div>
            <div>
                <button class="success" quest-id="${id}" class="">添加</button>
                <button class="warning" quest-id="${id}" class="">完成</button>
            </div>
        `
        o.innerHTML = content;
        step_list.appendChild(o);
    })
}