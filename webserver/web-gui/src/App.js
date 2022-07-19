// Import styplesheet for App
import './App.css';

// Import React for components
import React from 'react'

// Import Agent since it will be rendered in appb
import Agent from './Agent.js'

// Our top level class (gets rendered in index.html)
class App extends React.Component{

    // Constructor for component (set up what our App's state is)
    constructor(props) {
        super(props);
   
        // State contains a list of agents (json format), and a bool for if the data loaded
        this.state = {
            agents: [],
            DataisLoaded: false
        };
    }

    // When we renderour App, fetch the agent information
    componentDidMount() {
        // Fetch from our proxy (webserver.py, which when /agents is loaded will return our agents json information),
        fetch("/agents") // Shorthand for http://localhost:5000/agetns
            .then((res) => res.json()) // Result becomes a json
            .then((json) => { // take the json and set the state vars with it
                this.setState({
                    agents: json,
                    DataisLoaded: true
                });
            })
    }

    // Render Our App Component ( calls to Agent subchildren)
    render() {
        
        // Pull agents and the data loaded from our state (these were set in componentDidMount)
        const { DataisLoaded, agents } = this.state;
        
        // If our data didn't load, lets write HTML that we are waiting 
        if (!DataisLoaded) return <div>
            <h1> Please wait some time.... </h1> </div> ;
   
        // When our data is loaded, we want to return the HTML/REACT Calls for the APP
        return (

        // Div to clump app up into one component to render
        <div className = "App"> {/* Using app.css stylesheet */}
            {/* Header text */}
            <h1> Fetch data from an api in reacts </h1> {
                /* For every agent */
                agents.map((agent) => ( 
                    /* Render an Agent component, with props: agent_id, cur_angle, cur_pos, color */
                    <Agent agent_id={agent.agent_id} 
                           cur_angle={agent.cur_angle}
                           cur_pos={agent.cur_pos}
                           color={agent.color} />
                ))
            }
        </div>
    ); // End of return
}
}


// Allow it to be called in other functions
export default App;
