<style>
    h1 {
        text-align: center;
    }
    img{
        display: block;
        margin: auto;
        width: 40%;
        height: 40%;
    }
    .edit{
        background-color: rgb(72, 209, 72);
        float: right;
        margin-right: 20px;
        position: sticky;
        bottom: 20px;
        size: 200px;
    }

    .menu{
        background-color: rgb(211, 214, 211);
        float: left;
        margin-left: 20px;
        position: fixed;
        top: 20px;
        size: 200px;
    }
</style>

<h1>Habitat Maps for ODFW</h1>


<button class = "edit" onclick={() => window.location.href = '/edit'}>Edit</button>

<button class = "menu" onclick={() => window.location.href = '/menu'}>Menu</button>