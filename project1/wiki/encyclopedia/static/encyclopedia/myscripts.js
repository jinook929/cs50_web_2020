let originalEntries = document.querySelectorAll(".entry");
let search = "";

function myfunc() {
  let searchWord = document.querySelector("#searchWord").value;
  let entryList = document.getElementById("entryList");
  let entries = document.querySelectorAll(".entry");
  let details = document.querySelector('#details');
  search = searchWord.toLowerCase();
  clearAll(entries);

  if(details !== null) {
    let main = document.querySelector('.main');
    details.remove();
    entryList.remove();
    let h1 = document.createElement('h1');
    let heading = document.createTextNode("All Pages");
    h1.appendChild(heading);
    main.appendChild(h1);
    let eL = document.createElement('ul');
    eL.setAttribute("id", "entryList");
    main.appendChild(eL);
    filter(originalEntries);
    return;
  }

  if(search === "") {
    viewAll();
    return;
  }

  let tmp =[];
  originalEntries.forEach(entry => {
    if(entry.textContent.toLowerCase().includes(search)) {
      tmp.push(entry.textContent);
    }
  });

  if(tmp.length === 0) {
    let li = document.createElement("li");
    let entryName = document.createTextNode("No Entry Found");
    li.setAttribute("class", "entry");
    li.appendChild(entryName);
    entryList.appendChild(li);
    return;
  }

  filter(originalEntries);
}

function clearAll(entries) {
  entries.forEach(entry => {
    entry.remove();
  });
}

function viewAll() {
  for(let i = 0; i < originalEntries.length; i++) {
    let text = originalEntries[i].textContent;
    addLiNode(text);
  }
}

function addLiNode(text) {
  let a = document.createElement("a");
  let li = document.createElement("li");
  let entryName = document.createTextNode(text);
  a.appendChild(entryName);
  a.setAttribute("href", `/wiki/${text}`);
  li.appendChild(a);
  li.setAttribute("id", text);
  li.setAttribute("class", "entry");
  entryList.appendChild(li);
}

function filter(entries) {
  entries.forEach(entry => {
    let text = entry.textContent;
    if(text.toLowerCase().includes(search)) {
      addLiNode(text);
    } else {
      entry.remove();
    }
  });
}