<script lang="ts">
    import * as d3 from 'd3';
    // onmount to initalize map
    import {onMount} from 'svelte';
    // SVG element reference for the map
    let svgE1: SVGElement;


    onMount(async function() {
        // where all the map data is loaded and manipulated
        const response = await fetch('/watershed.geojson');
        const json = await response.json();

        // path and projection (just where its placed)
        const projection = d3.geoMercator().fitSize([900, 600], json);
        const path = d3.geoPath().projection(projection);

        // select the SVG element
        const svg = d3.select(svgE1);

        // rendering the watershed features
        svg.selectAll('path')
            .data(json.features)
            .enter()
            .append('path')
            .attr('d', path as any)
            .attr('fill', 'white')
            .attr('stroke', 'black');

        // mouse clicking for each huc double click to get rid of the selection
        svg.selectAll('path')
            .on('click', function() {
                d3.select(this).attr('fill', 'orange');
            })
            .on('dblclick', function() {
                d3.select(this).attr('fill', 'white');
                
            })
            ;

        // hover tooltip for each name
        // can be later 


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
        align-items: center;
    }

    .tooltip{
        font-size: 12px;
    }

</style>

<div class = main>

<h1>Habitat Maps for ODFW</h1>

<!-- container for the map -->
<svg bind:this={svgE1} class = "map" width="900" height="600"></svg>

<!-- <button class = "edit" onclick={() => window.location.href = '/edit'}>Edit</button> -->

<!-- <button class = "menu" onclick={() => window.location.href = '/menu'}>Menu</button> -->

</div>