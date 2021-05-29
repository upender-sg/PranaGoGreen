$( document ).ready(function(){
     $("[id^=cartdelete_]").click(function(){
        ///itemclear/{{ value.product_id }}?next=cartdetail
        pid = this.id.split("_")[1]
        alert(pid)
        $.get('/itemclear/'+pid,{'id':pid} , function(data){
            
            location.reload();

        })
     })
})