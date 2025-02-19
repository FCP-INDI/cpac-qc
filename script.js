document.addEventListener("DOMContentLoaded", function () {
    var subjectTabs = document.getElementById("subjectTabs");
    var tabContentContainer = document.getElementById("tabContentContainer");
    var activeSubject = null;
    var selectedImageNames = [];

    var csvPath = "results.csv";
    d3.csv(csvPath).then(function (csv) {
        // Extract unique subjects from the CSV data and sort them
        var subjects = Array.from(new Set(csv.map((d) => d.sub))).sort();

        subjects.forEach(function (subject, index) {
            var tab = document.createElement("li");
            tab.className = "nav-item";
            var tabIndex = index === 0 ? "active" : "";
            tab.innerHTML = `<a class="nav-link ${tabIndex}" id="${subject}-tab" data-toggle="tab" href="#${subject}" role="tab" aria-controls="${subject}" aria-selected="true">${subject}</a>`;
            subjectTabs.appendChild(tab);

            var tabContent = document.createElement("div");
            tabContent.className = `tab-pane fade ${tabIndex}`;
            tabContent.id = subject;
            tabContentContainer.appendChild(tabContent);

            tab.addEventListener("click", function () {
                if (activeSubject !== subject) {
                    openTab(subject);
                }
            });

            if (index === 0) {
                activeSubject = subject;
            }
        });

        // Open the first tab by default
        if (subjects.length > 0) {
            openTab(subjects[0]);
        }

        var allImages = Array.from(new Set(csv.map((d) => d.relative_path.split("/").pop().replace(".png", "")))).sort();
        var form = document.getElementById("imageSelectionForm");

        allImages.forEach(function (imageName) {
            var checkbox = document.createElement("div");
            checkbox.className = "form-check";
            checkbox.innerHTML = `
                <input class="form-check-input" type="checkbox" value="${imageName}" id="${imageName}" checked>
                <label class="form-check-label" for="${imageName}">
                    ${imageName}
                </label>`;
            form.appendChild(checkbox);
        });

        // Add event listener to the apply button in the sidebar
        document.getElementById("applySelectionButton").addEventListener("click", function () {
            selectedImageNames = Array.from(document.querySelectorAll("#imageSelectionForm input:checked")).map((input) => input.value);
            if (selectedImageNames.length === 0) {
                document.getElementById("noSelectionMessage").style.display = "block";
            } else {
                document.getElementById("noSelectionMessage").style.display = "none";
                filterImagesByImageNames(selectedImageNames, csv, activeSubject);
            }
        });

        // Add event listeners for select all and deselect all buttons
        document.getElementById("selectAllButton").addEventListener("click", function () {
            document.querySelectorAll("#imageSelectionForm input[type='checkbox']").forEach(function (checkbox) {
                checkbox.checked = true;
            });
        });

        document.getElementById("deselectAllButton").addEventListener("click", function () {
            document.querySelectorAll("#imageSelectionForm input[type='checkbox']").forEach(function (checkbox) {
                checkbox.checked = false;
            });
        });
    });

    function openTab(tabName) {
        var tabs = document.querySelectorAll(".tab-pane");

        for (var i = 0; i < tabs.length; i++) {
            tabs[i].classList.remove("show", "active");
        }

        var tabContent = document.getElementById(tabName);
        if (tabContent) {
            tabContent.classList.add("show", "active");
            tabContent.innerHTML = "";
            console.log("Opening tab:", tabName);

            activeSubject = tabName;

            var csvPath = "results.csv";
            d3.csv(csvPath).then(function (csv) {

                if (Array.isArray(csv)) {
                    var uniqueSesScanReg = Array.from(
                        new Set(
                            csv
                                .filter((d) => d.sub == tabName)
                                .map((d) => `${d.ses}`)
                        )
                    ).sort();

                    // Loop over the uniqueSesScanReg and create a row for each
                    for (var i = 0; i < uniqueSesScanReg.length; i++) {
                        var rowContainer = document.createElement("div");
                        rowContainer.className = "row";

                        var sesScanReg = uniqueSesScanReg[i];
                        var images = csv.filter((d) => d.sub == tabName && d.ses == sesScanReg).sort((a, b) => a.file_name.localeCompare(b.file_name));

                        images.forEach(function (imageData) {
                            var imageName = imageData.file_name;
                            var imagePath = `./${imageData.relative_path}`;

                            var imageContainer = document.createElement("div");
                            imageContainer.className = "col-md-4 col-12";
                            imageContainer.innerHTML = `
                                <div style="padding: 10px;">
                                    <img src="${imagePath}" class="img-fluid" style="padding: 10px;" onerror="this.onerror=null; this.src=''; console.error('Image not found:', '${imagePath}');" />
                                    <h6 style="padding: 1px;">${imageName}</h6>
                                </div>`;
                            rowContainer.appendChild(imageContainer);
                        });

                        // Append rowContainer to tabContent
                        tabContent.appendChild(rowContainer);
                    }

                    // Reapply the filter if images are selected
                    if (selectedImageNames.length > 0) {
                        filterImagesByImageNames(selectedImageNames, csv, activeSubject);
                    }
                } else {
                    console.error("CSV data is not an array:", csv);
                }
            });
        } else {
            console.error(`Tab content with ID ${tabName} not found.`);
        }
    }

    function filterImagesByImageNames(imageNames, csv, subject) {
        var tabContent = document.getElementById(subject);
        if (tabContent) {
            tabContent.innerHTML = "";

            var filteredImages;
            if (imageNames.length === 0) {
                filteredImages = csv.filter((d) => d.sub === subject);
            } else {
                filteredImages = csv.filter((d) => imageNames.includes(d.relative_path.split("/").pop().replace(".png", "")) && d.sub === subject);
            }

            var rowContainer = document.createElement("div");
            rowContainer.className = "row";

            filteredImages.forEach(function (imageData) {
                var imageName = imageData.file_name;
                var imagePath = `./${imageData.relative_path}`;

                var imageContainer = document.createElement("div");
                imageContainer.className = "col-md-4 col-12";
                imageContainer.innerHTML = `
                    <div style="padding: 10px;">
                        <img src="${imagePath}" class="img-fluid" style="padding: 10px;" onerror="this.onerror=null; this.src=''; console.error('Image not found:', '${imagePath}');" />
                        <h6 style="padding: 1px;">${imageName}</h6>
                    </div>`;
                rowContainer.appendChild(imageContainer);
            });

            tabContent.appendChild(rowContainer);
        } else {
            console.error(`Tab content with ID ${subject} not found.`);
        }
    }
});