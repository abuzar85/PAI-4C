class SearchTree {
    constructor(svgId, containerId) {
        this.svg = d3.select(`#${svgId}`);
        this.container = document.getElementById(containerId);
        this.width = this.container.clientWidth;
        this.height = this.container.clientHeight;

        this.g = this.svg.append("g");

        // Zoom and Pan
        this.zoom = d3.zoom()
            .scaleExtent([0.1, 3])
            .on("zoom", (event) => {
                this.g.attr("transform", event.transform);
            });

        this.svg.call(this.zoom);

        this.nodes = [];
        this.links = [];
        this.idToNode = new Map();

        this.treeLayout = d3.tree().nodeSize([40, 60]);
    }

    reset() {
        this.nodes = [];
        this.links = [];
        this.idToNode.clear();
        this.g.selectAll("*").remove();
        this.svg.call(this.zoom.transform, d3.zoomIdentity);
    }

    addNode(id, parentId, data) {
        const node = { id, parentId, ...data };
        this.nodes.push(node);
        this.idToNode.set(id, node);

        if (parentId !== null && this.idToNode.has(parentId)) {
            this.links.push({ source: parentId, target: id });
        }

        this.update();
    }

    update() {
        // Create hierarchy
        const stratify = d3.stratify()
            .id(d => d.id)
            .parentId(d => d.parentId);

        if (this.nodes.length === 0) return;

        const root = stratify(this.nodes);
        this.treeLayout(root);

        // Links
        const link = this.g.selectAll(".link")
            .data(root.links(), d => d.target.id);

        link.enter().append("path")
            .attr("class", "link")
            .attr("d", d3.linkVertical()
                .x(d => d.x + this.width / 2)
                .y(d => d.y + 50));

        link.attr("d", d3.linkVertical()
            .x(d => d.x + this.width / 2)
            .y(d => d.y + 50));

        // Nodes
        const node = this.g.selectAll(".node")
            .data(root.descendants(), d => d.id);

        const nodeEnter = node.enter().append("g")
            .attr("class", d => `node ${d.data.type}`)
            .attr("transform", d => `translate(${d.x + this.width / 2}, ${d.y + 50})`)
            .on("mouseover", (event, d) => this.showTooltip(event, d))
            .on("mouseout", () => this.hideTooltip());

        nodeEnter.append("circle")
            .attr("r", 5);

        node.attr("class", d => `node ${d.data.type} ${d.data.active ? 'active' : ''}`)
            .transition()
            .duration(300)
            .attr("transform", d => `translate(${d.x + this.width / 2}, ${d.y + 50})`);

        // Center on the newest active node
        const activeNode = this.nodes.find(n => n.active);
        if (activeNode) {
            // Logic to move zoom could go here if needed
        }
    }

    setActiveNode(id, type) {
        this.nodes.forEach(n => {
            n.active = (n.id === id);
            if (n.id === id && type) n.type = type;
        });
        this.update();
    }

    showTooltip(event, d) {
        const tooltip = d3.select("body").append("div")
            .attr("class", "tree-tooltip")
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 10) + "px");

        tooltip.html(`
            <strong>Node ID:</strong> ${d.data.id}<br>
            <strong>Step:</strong> ${d.data.description || 'N/A'}
        `);
    }

    hideTooltip() {
        d3.selectAll(".tree-tooltip").remove();
    }
}
