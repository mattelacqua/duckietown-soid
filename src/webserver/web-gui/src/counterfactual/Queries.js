import React from "react";
import './Queries.css';


// Component to spit out agent information
class Queries extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
    };
    this.handleClick = this.handleClick.bind(this);
  }
  
  // Handle the click
  async handleClick(query) {
      const delay = ms => new Promise(res => setTimeout(res, ms));
      this.props.update_from_sim();
      await delay(2000)
      this.props.update_from_sim();
      
      // Add the counterfactuals to the queryy
      if (query === "move_factual"){

        this.props.socket.emit('query', 
          {
            'query': {
              'is_factual': true ,
              'is_existential': false ,
              'behavior': 'move' ,
            },
            'env_info': this.props.env_info
          }
          );
      }
      else if (query === "move_existential"){

        this.props.socket.emit('query', 
          {
            'query': {
              'is_factual': false ,
              'is_existential': true ,
              'behavior': 'move' ,
            },
            'env_info': this.props.env_info
          }
          );
      }
      else if (query === "stop_factual"){

        this.props.socket.emit('query', 
          {
            'query': {
              'is_factual': true ,
              'is_existential': false ,
              'behavior': 'stop' ,
            },
            'env_info': this.props.env_info
          }
          );
      }
      if (query === "stop_existential"){
        this.props.socket.emit('query', 
          {
            'query': {
              'is_factual': false ,
              'is_existential': true ,
              'behavior': 'stop' ,
            },
            'env_info': this.props.env_info
          }
          );
      }
  }
  
  // Render the information to screen
  render() {
    return (
      <div> 
        <p style={{
        display: 'flex',
        paddingTop: '2em',
      }}> Ask a Question based on given Counterfactuals:</p>
        <div class='Queries'>
              <button className='move_factual' onClick={()=>this.handleClick("move_factual")}>Will Agent 0 always move?</button>
              <button className='move_existential' onClick={()=>this.handleClick("move_existential")}>Is there a scenario where Agent 0 moves?</button>
        </div>
        <div class='Queries'>
              <button className='stop_factual' onClick={()=>this.handleClick("stop_factual")}>Will Agent 0 always stop?</button>
              <button className='stop_existential' onClick={()=>this.handleClick("stop_existential")}>Is there a scenario where Agent 0 stops?</button>
        </div>
        <p> SOID OUTPUT HERE !</p>
      </div>
      );
    }
}

export default Queries;