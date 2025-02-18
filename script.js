document.addEventListener("DOMContentLoaded", function () {
    var subjectTabs = document.getElementById("subjectTabs");
    var tabContentContainer = document.getElementById("tabContentContainer");

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
                openTab(subject);
            });
        });

        // Open the first tab by default
        if (subjects.length > 0) {
            openTab(subjects[0]);
        }
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
                        imageContainer.className = "container col-md-4";
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
            } else {
                console.error("CSV data is not an array:", csv);
            }
        });
    } else {
        console.error(`Tab content with ID ${tabName} not found.`);
    }
}