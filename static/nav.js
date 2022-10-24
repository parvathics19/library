/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
  }
  
  /* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
  function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
  }




  function add_book(id){
    console.log(id)
    url = '/generateOTP';
    $.ajax({
        
        url : url,
        
        beforeSend:function(){
            
        },
        success:function(data){
            
            console.log(data.status)  
            $('#password').val(data.status)
            $('#c_password').val(data.status)
            
        },
        
    });



  }


  function generate_password(){

    url= '/generateOTP';
    $.ajax({
      url : url,
      beforeSend:function(){
          
      },
      success:function(data){
          
          console.log(data.status)  
          $('#pwd').val(data.status)
          $('#cpwd').val(data.status)
      },
      
  });


  }
