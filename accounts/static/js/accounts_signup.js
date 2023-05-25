function search_address() {
  new daum.Postcode({
    oncomplete: function(data) {
      const addr = data.address;
      document.getElementById("s_address").value = addr;
      const addt = data.bname;
      document.getElementById("t_address").value = addt;
      const addb = data.buildingName;
      document.getElementById("b_address").value = addb;
    }
  }).open();
}