<script lang="ts">
    import * as d3 from 'd3';
    import {onMount} from 'svelte';
    let svgE1: SVGElement;


    onMount(async function() {
        // where all the map data is loaded and manipulated
        const response = await fetch('/watershed.geojson');
        const json = await response.json();
        const projection = d3.geoMercator().fitSize([900, 600], json);
        const path = d3.geoPath().projection(projection);

        const svg = d3.select(svgE1);

        svg.selectAll('path')
            .data(json.features)
            .enter()
            .append('path')
            .attr('d', path as any)
            .attr('fill', 'white')
            .attr('stroke', 'black');
    });


</script>

<style>
    h1 {
        text-align: center;
    }

    .menu{
        background-color: rgb(211, 214, 211);
        float: left;
        margin-left: 20px;
        position: fixed;
        top: 20px;
        size: 200px;
    }

    .map{
        border: 1px solid black;
        display: block;
    }

</style>

<div class = main>

<h1>Habitat Maps for ODFW</h1>

<svg bind:this={svgE1} class = "map" width="900" height="600"></svg>

<!-- <button class = "edit" onclick={() => window.location.href = '/edit'}>Edit</button> -->

<!-- <button class = "menu" onclick={() => window.location.href = '/menu'}>Menu</button> -->

</div>