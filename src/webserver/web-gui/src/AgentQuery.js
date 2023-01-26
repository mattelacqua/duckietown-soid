// Import style
import './Agent.css';
// Import React
import React from "react";

// Import Query stuff
import AddQuery from './AddQuery.js'
import QueryList from './AddQuery.js'

// Agent Component (gets rendered in app)
class AgentQuery extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    // I don't think it will have a ton of stuff in its state. It might change, but i think it should be good.
    this.state = {
      agent_id: props.agent_id,
    };
  }

  // Render the agent component (Wrapper to add a query, and one to edit the query list)
  render() {

    /* Add Query: 
          - We are passing all the info through so that we can prefil text boxes with the values here.
          - We pass counterfactuals list through so we can add one on at the very end with a button.
      Query list:
          - Map through all the queries and their information and display to the user so they can get rid of ones they no longer want.
    */
    return (
            <div>
                <AddQuery   agent_id={this.props.agent_id}
                            id={this.props.agent_id}
                            pos_x={this.props.pos_x}
                            pos_z={this.props.pos_z}
                            prev_pos_x={this.props.prev_pos_x}
                            prev_pos_z={this.props.prev_pos_z}
                            stop_x={this.props.stop_x}
                            stop_z={this.props.stop_z}
                            tile_x={this.props.tile_x}
                            tile_z={this.props.tile_z}
                            angle={this.props.angle}
                            angle_deg={this.props.angle_deg}
                            speed={this.props.speed}
                            forward_step={this.props.forward_step}
                            direction={this.props.direction}
                            intersection_arrival={this.props.intersection_arrival}
                            patience={this.props.patience}
                            step_count={this.props.step_count}
                            lookahead={this.props.lookahead}
                            states={this.props.states}
                            exists={this.props.exists}
                            color={this.props.color} 
                            turn_choice={this.props.turn_choice} 
                            signal_choice={this.props.signal_choice} 
                            lights={this.props.lights} 
                            counterfactuals={this.props.counterfactuals} 
                            bbox_w={this.props.bbox_w} 
                            bbox_l={this.props.bbox_l} />
                  <QueryList 
                              agent_id={this.props.agent_id} 
                              index={this.props.agent_id} 
                              counterfactuals={this.props.counterfactuals} 
                              socket={this.props.socket}/>
             </div>
          );
    }
}

// Allow it to be called in other functions
export default AgentQuery;
