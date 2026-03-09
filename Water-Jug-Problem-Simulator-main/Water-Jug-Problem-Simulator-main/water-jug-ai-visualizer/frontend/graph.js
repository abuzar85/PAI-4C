class StateGraph {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.width = this.container.clientWidth;
        this.height = this.container.clientHeight;

        this.svg = d3.select(`#${containerId}`)
            .append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", `0 0 ${this.width} ${this.height}`);

        this.g = this.svg.append("g");

        // Zoom functionality
        this.svg.call(d3.zoom().on("zoom", (event) => {
            this.g.attr("transform", event.transform);
        }));

        this.simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(d => d.id).distance(80))
            .force("charge", d3.forceManyBody().strength(-200))
            .force("center", d3.forceCenter(this.width / 2, this.height / 2))
            .force("collision", d3.forceCollide().radius(30));

        this.nodes = [];
        this.links = [];
        this.nodeElements = this.g.append("g").attr("class", "nodes");
        this.linkElements = this.g.append("g").attr("class", "links");
    }

    reset() {
        this.nodes = [];
        this.links = [];
        this.update();
    }

    addState(state, parentState = null, isTarget = false) {
        const stateStr = `(${state[0]}, ${state[1]})`;

        // Don't add if already exists in graph (though traversal might visit it)
        let node = this.nodes.find(n => n.id === stateStr);
        if (!node) {
            node = { id: stateStr, state: state, isTarget: isTarget };
            this.nodes.push(node);
        }

        if (parentState) {
            const parentStr = `(${parentState[0]}, ${parentState[1]})`;
            const linkExists = this.links.some(l => l.source === parentStr && l.target === stateStr);
            if (!linkExists) {
                this.links.push({ source: parentStr, target: stateStr });
            }
        }

        this.update();
        return stateStr;
    }

    update() {
        // Links
        const link = this.linkElements.selectAll("line")
            .data(this.links, d => `${d.source}-${d.target}`);

        link.exit().remove();
        const linkEnter = link.enter().append("line")
            .attr("class", "link");

        const mergedLinks = linkEnter.merge(link);

        // Nodes
        const node = this.nodeElements.selectAll(".node")
            .data(this.nodes, d => d.id);

        node.exit().remove();
        const nodeEnter = node.enter().append("g")
            .attr("class", d => `node ${d.isTarget ? 'node--target' : ''}`)
            .call(d3.drag()
                .on("start", (e, d) => this.dragstarted(e, d))
                .on("drag", (e, d) => this.dragged(e, d))
                .on("end", (e, d) => this.dragended(e, d)));

        nodeEnter.append("circle")
            .attr("r", 15)
            .attr("fill", "#1e293b");

        nodeEnter.append("text")
            .attr("dy", 4)
            .attr("text-anchor", "middle")
            .text(d => d.id);

        const mergedNodes = nodeEnter.merge(node);

        this.simulation.nodes(this.nodes);
        this.simulation.force("link").links(this.links);
        this.simulation.alpha(1).restart();

        this.simulation.on("tick", () => {
            mergedLinks
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            mergedNodes
                .attr("transform", d => `translate(${d.x},${d.y})`);
        });
    }

    highlightState(state) {
        const stateStr = `(${state[0]}, ${state[1]})`;
        this.nodeElements.selectAll(".node")
            .classed("node--active", d => d.id === stateStr);

        this.linkElements.selectAll("line")
            .classed("link--active", d => d.target.id === stateStr);
    }

    dragstarted(event, d) {
        if (!event.active) this.simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    dragended(event, d) {
        if (!event.active) this.simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}
