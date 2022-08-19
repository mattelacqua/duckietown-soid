import React from "react";
import './Buttons.css';
import { Test, QuestionGroup, Question, Option } from 'react-multiple-choice';

import io from 'socket.io-client';

const socket = io();

// Component to spit out agent information
class TurnChoice extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
        agent_id: this.props.agent_id,
        turn_choice: this.props.turn_choice,
    };
    this.handleChoice = this.handleChoice.bind(this);
  }

  // Handle the click
  handleChoice(turn) {
    this.setState({
      turn_choice: turn,
    });
    socket.emit('turn_choice',
        {
            'agent_id':this.state.agent_id,
            'turn':turn,
        });
  }
  
  // Render the information to screen
  render() {
    return (
        <Test onOptionSelect={selectedOptions => this.handleChoice(selectedOptions)}>
          <QuestionGroup questionNumber={0}>
            <Question>Turn Choice</Question>
            <Option value="Right">Right</Option>
            <div>Add some additional info or tooltips for specific questions</div>
            <Option value="Left">Left</Option>
            <Option value="Straight">Straight</Option>
            <Option value="Random">Random</Option>
          </QuestionGroup>
        </Test>
    );
  }
}


export default TurnChoice;
