// Import style
import './AngleDial.css';
import './AgentMap.css'

// Import React
import React from "react";

import AngleDial from './AngleDial.js'

class AngleDialAgents extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
        };
        }


    render() {
        return (

        <><span class='text'> Drag and Drop Position / Angle Adjustments </span>

        <div class="angle-dialwrap">
                {this.props.agents.map((agent) => (
                    <AngleDial agent={agent}
                        socket={this.props.socket} />
                ))}

            </div></>
      
        )

        }
    }

    export default AngleDialAgents;


/* <span class =  'text'> Drag and Drop Position / Angle Adjustments </span> 

<div class = "angle-dialwrap">
  {this.props.agents.map((agent) => ( 
    <AngleDial  agent={agent}
                socket={this.props.socket}
                />
  ))}

</div> */
