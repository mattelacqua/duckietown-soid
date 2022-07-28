import React from "react";


// Component to spit out agent information
class RenderedScene extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      src: "http://localhost:5000/renderedScene",
      key: Date.now(),
    };

    this.tick = this.tick.bind(this);
  }

  tick() {
    this.setState({
      src: "http://localhost:5000/renderedScene",
      key: Date.now(),
    }) 
  }
  
  componentDidMount() {
    this.interval = setInterval(() => this.tick(), 500);
  }
  
  // Render the information to screen
  render() {
    return (
      <div
        style={{
              height: '600px',
              width: '800px',
              //backgroundImage: "url('http://localhost:5000/mapImageBackground')",
              background: "white",
            }}>
          {/* HTML FOR IMAGE */}
          <img src={this.state.src + "?v=" + this.state.key} /> 
      </div>
      );
    }
}


export default RenderedScene;
