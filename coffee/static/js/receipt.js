const printReceiptButton = document.querySelector("#print-receipt");

printReceiptButton?.addEventListener("click", () => {
    window.print();
});
