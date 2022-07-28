// Import styplesheet for App
import './App.css';

// Import React for components
import React from 'react'

// Import Agent since it will be rendered in appb
import Agent from './Agent.js'

// Import Environment since it will be rendered in app
import Environment from './Environment.js'

// Import Agentmpa
import AgentMap from './AgentMap.js'

// Import RenderedScene
import RenderedScene from './RenderedScene.js'
// Our top level class (gets rendered in index.html)
class App extends React.Component{

    // Constructor for component (set up what our App's state is)
    constructor(props) {
        super(props);
   
        // State contains a list of agents (json format), and a bool for if the data loaded
        this.state = {
            agents: [],
            env_info: [],
            AgentsLoaded: false,
            EnvLoaded: false,
            rendred_imgLoaded: false,
            rendered_img: new Image(),
        };
        this.pos_pass = this.pos_pass.bind(this); // Bind angle pass to this component
    }

    // When we renderour App, fetch the agent information
    componentDidMount() {
        // Fetch from our proxy (webserver.py, which when /agents is loaded will return our agents json information),
        fetch("/agents") // Shorthand for http://localhost:5000/agetns
            .then((res) => res.json()) // Result becomes a json
            .then((json) => { // take the json and set the state vars with it
                this.setState({
                    agents: json,
                    AgentsLoaded: true
                });
            });

        // Fetch for env info
        fetch("/envInfo") // Shorthand for http://localhost:5000/agetns
            .then((res) => res.json()) // Result becomes a json
            .then((json) => { // take the json and set the state vars with it
                this.setState({
                    env_info: json,
                    EnvLoaded: true
                });
            });

      // Get the rendered image
      const image = new Image();
      image.src = 'http://localhost:5000/renderedScene';
      this.setState({
        rendered_img: image,
        rendered_imgLoaded: true
      });
    }
   
    pos_pass(id, x, y) {
      let agents = [...this.state.agents];
      let agent = {...agents[id]};
      agent.cur_pos = {'x': x, 
                       'y': y}
      agents[id] = agent;
      this.setState({agents});
      console.log(this.state.agents);
    }

    // Render Our App Component ( calls to Agent subchildren)
    render() {
        
        // Pull agents and the data loaded from our state (these were set in componentDidMount)
        const { AgentsLoaded, EnvLoaded, rendered_imgLoaded, agents, env_info, rendered_img} = this.state;
        
        // If our data didn't load, lets write HTML that we are waiting 
        if (!AgentsLoaded) return <div>
            <h1> Please wait some time to load Agent information.... </h1> </div> ;

        if (!EnvLoaded) return <div>
            <h1> Please wait some time to load Environmen information.... </h1> </div> ;
   
        if (!rendered_imgLoaded) return <div>
            <h1> Please wait some time to load Rendered Scene .... </h1> </div> ;
        // When our data is loaded, we want to return the HTML/REACT Calls for the APP
        return (

        // Div to clump app up into one component to render
        <div className = "App"> {/* Using app.css stylesheet */}
            {/* Header text */}
            <h1> SCENE </h1> 
          {/*<RenderedScene />*/}
            <h1> Fetch data from an api in reacts </h1> 
              <Environment  max_NS={env_info.max_NS} 
                            max_EW={env_info.max_EW} 
                            tile_size={env_info.tile_size}/>
              <AgentMap agents={agents} 
                        max_NS={env_info.max_NS} 
                        max_EW={env_info.max_EW} 
                        tile_size={env_info.tile_size} 
                        pos_pass={this.pos_pass}/>
                {
                agents.map((agent) => ( 
                    /* Render an Agent component, with props: agent_id, cur_angle, cur_pos, color */
                    <Agent agent_id={agent.agent_id} 
                           cur_angle={agent.cur_angle}
                           cur_pos={agent.cur_pos}
                           color={agent.color} 
                           lights={agent.lights} />
                ))
            }

        </div>
    ); // End of return
}
}


// Allow it to be called in other functions
export default App;
