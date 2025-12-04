// Home Page Function

document.addEventListener("DOMContentLoaded", () => {

    // Clear Search Results / Blog Message Function
    const clearBtn = document.querySelector(".clearBtn");
    if (clearBtn) {
        clearBtn.addEventListener("click", () => {
            const title = document.querySelector("#searchTitle");
            if (title) title.innerHTML = "";

            document.querySelectorAll(".searchName").forEach(el => el.innerHTML = "");
            document.querySelectorAll(".searchFact").forEach(el => el.innerHTML = "");
        });
    }

    // Registration Page Functions
    // Reveal help icons

    document.querySelectorAll(".btnInfo").forEach(button => {
        button.addEventListener("click", (event) => {
            const id = event.target.dataset.type;
            const helpBox = document.getElementById(id);
            if (helpBox){
                helpBox.classList.toggle("hidden")
            }
        });
    });

    // Reveal Password Input
    document.querySelectorAll(".revealPass").forEach(checkbox => {
        checkbox.addEventListener("click", function () {
            const id = this.dataset.type;
            const field = document.getElementById(id);
            if (field) {
                if (field.type === "password") {
                    field.type = "text"
                } else {
                    field.type = "password"
                }
            }
        });
    });

    // Clear Comment Function
    const cancelBtn = document.querySelector(".btnCancel");
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function () {
            const id = this.dataset.type;
            const field = document.getElementById(id);
            if (field) {
                field.value = ""
            }
        });
    }

});

