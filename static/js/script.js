// Home Page Function
// Clear Search Results / Blog Message Function

document.querySelector(".clearBtn").addEventListener('click', ()=> {
    document.querySelector("#searchTitle").innerHTML = ""

    document.querySelectorAll(".searchName").forEach((element) => {
        element.innerHTML = "";
    });
    document.querySelectorAll(".searchFact").forEach((element) => {
        element.innerHTML = "";
    });
})

// Registration Page Functions
// Reveal help icons

document.querySelectorAll('.btnInfo').forEach((button) =>{
    button.addEventListener('click', (event) => {
        const ibtn_selected_type = event.target.dataset.type;
        const ibtn_element = document.getElementById(ibtn_selected_type);
        if (ibtn_element.style.display === "none"){
            ibtn_element.style.display = "block"
        } else {
            ibtn_element.style.display = "none"
        }
    })
})

// Reveal Password Input

document.querySelectorAll('.reavealPass').forEach((button) =>{
    button.addEventListener('click', () => {
        const ibtn_selected_type = this.dataset.type;
        const ibtn_element = document.getElementById(ibtn_selected_type);
        if (ibtn_element.style.display === "none"){
            ibtn_element.style.display = "block"
        } else {
            ibtn_element.style.display = "none"
        }
    })
})

// Blog Page
// Delete Blog Function

document.querySelector(".deleteBtn").addEventListener('click',()=>{
        if (confirm("Are you sure you want to delete this Blog?")){
            document.getElementById("completedDelete").submit()
        }
    })

// Clear Comment Function

document.querySelector(".btnCancel").addEventListener('click',()=>{
    const ibtn_selected_type = this.dataset.type;
    document.getElementById(ibtn_selected_type).value = ""
})


/*
function clearSearch(){
    document.querySelector("#searchTitle").innerHTML = ""

    document.querySelectorAll(".searchName").forEach((element) => {
        element.innerHTML = "";
    });
    document.querySelectorAll(".searchFact").forEach((element) => {
        element.innerHTML = "";
    });
}


// Registration Page Functions
// Reveal help icons

function toggleHelp(selected_type){
    const ibtn_element = document.getElementById(selected_type);
    if (ibtn_element.style.display === "none"){
        ibtn_element.style.display = "block"
    } else {
        ibtn_element.style.display = "none"
    }
}

// Reveals password input

function revealPassword(selected_type){
    const reveal_input = document.getElementById(selected_type)
    if(reveal_input.type == "password"){
        reveal_input.type = "text";
    } else {
        reveal_input.type = "password";
    }
}

*/