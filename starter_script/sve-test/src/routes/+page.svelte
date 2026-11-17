<!-- The main code-->

<script lang="ts">
	import kit_fox from '#lib/assets/kit_fox.png';
</script>

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
    button{
        background-color: rgb(72, 209, 72);
        float: right;
        margin-right: 20px;
        position: sticky;
        bottom: 20px;
        size: 200px;
    }
</style>

<h1>Habitat Maps for ODFW</h1>

<img src={kit_fox} alt="Oregon Map of the Kit Fox Habitat" />

<button onclick={() => window.location.href = '/edit'}>Edit</button>