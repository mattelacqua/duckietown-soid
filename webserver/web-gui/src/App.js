// Import styplesheet for App
import './App.css';

// Import React for components
import React from 'react'

// Import Agents since it will be rendered in appb
import Agents from './Agents.js'

// Import Environment since it will be rendered in app
import Environment from './Environment.js'

// Import Agentmpa
import AgentMap from './AgentMap.js'

// Import RenderedScene
import RenderedScene from './RenderedScene.js'

// Import RenderedScene
import Buttons from './Buttons.js'

// Import LODASH
import _ from 'lodash';

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
            sim_state: "run",
        };
        this.pos_pass = this.pos_pass.bind(this); // Bind pos pass to this component
        this.sim_state_pass = this.sim_state_pass.bind(this); // Bind pos pass to this component
        this.update_from_sim = this.update_from_sim.bind(this); // Bind this to update_from sim 
    }

    // Update from the simulator
    update_from_sim() {
       // Fetch from our proxy (webserver.py, which when /agents is loaded will return our agents json information),
      fetch("/agents") // Shorthand for http://localhost:5000/agetns
          .then((res) => res.json()) // Result becomes a json
          .then((json) => { // take the json and set the state vars with it
              let new_ref = json; // Set a new reference so that it will recognize change and update in children.
              if (!_.isEqual(new_ref, this.state.agents)) {
                console.log("NEW Agents INFO", new_ref);
                this.setState({
                    agents: new_ref,
                    AgentsLoaded: true
                });
              } // Endif
          });

      // Fetch for env info
      fetch("/envInfo") // Shorthand for http://localhost:5000/agetns
          .then((res) => res.json()) // Result becomes a json
          .then((json) => { // take the json and set the state vars with it
              let new_ref = json;
              if (!_.isEqual(new_ref, this.state.env_info)) {
                console.log("NEW ENV INFO", new_ref);
                this.setState({
                    env_info: new_ref,
                    EnvLoaded: true
                });
              } // Endif
          });

      // Get the rendered image
      const image = new Image();
      image.src = 'http://localhost:5000/renderedScene';
      this.setState({
        rendered_img: image,
        rendered_imgLoaded: true
      });

      this.forceUpdate();

    }
    // When we renderour App, fetch the agent information
    componentDidMount() {
      this.interval = setInterval(() => this.update_from_sim(), 5000);
    }
   
    sim_state_pass(state) {
      this.setState({sim_state: state});
      console.log("Sim State:", this.state.sim_state);
    }
 
    // Pass the position change into agent state
    pos_pass(id, x, y) {
      let new_agents = [...this.state.agents];
      let agent = {...new_agents[id]};
      agent.cur_pos = {'x': x, 
                       'y': y}
      new_agents[id] = agent;
      this.setState({agents: new_agents});
    } 
    // Render Our App Component ( calls to Agent subchildren)
    render() {
        
        
        // If our data didn't load, lets write HTML that we are waiting 
        if (!this.state.AgentsLoaded) return <div>
            <h1> Please wait some time to load Agent information.... </h1> </div> ;

        if (!this.state.EnvLoaded) return <div>
            <h1> Please wait some time to load Environmen information.... </h1> </div> ;
   
        if (!this.state.rendered_imgLoaded) return <div>
            <h1> Please wait some time to load Rendered Scene .... </h1> </div> ;
        // When our data is loaded, we want to return the HTML/REACT Calls for the APP
        return (

        // Div to clump app up into one component to render
        <div className = "App"> {/* Using app.css stylesheet */}
            {/* Header text */}
            <h1> SCENE </h1> 

            <Buttons sim_state={this.state.sim_state} 
                     sim_state_pass={this.sim_state_pass}
                     update_from_sim={this.update_from_sim}/>

            <RenderedScene />

            <h1> Fetch data from an api in reacts </h1> 
              <Environment  max_NS={this.state.env_info.max_NS} 
                            max_EW={this.state.env_info.max_EW} 
                            tile_size={this.state.env_info.tile_size}/>
                            sim_state={this.state.sim_state}/>
              <AgentMap agents={this.state.agents} 
                        max_NS={this.state.env_info.max_NS} 
                        max_EW={this.state.env_info.max_EW} 
                        tile_size={this.state.env_info.tile_size} 
                        pos_pass={this.pos_pass}/>
             <Agents agents={this.state.agents}/>

        </div>
    ); // End of return
}
}


// Allow it to be called in other functions
export default App;
