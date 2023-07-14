// Auto-generated. Do not edit!

// (in-package learning_tf2.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class evaluateSLAMEvoRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.cmd = null;
    }
    else {
      if (initObj.hasOwnProperty('cmd')) {
        this.cmd = initObj.cmd
      }
      else {
        this.cmd = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type evaluateSLAMEvoRequest
    // Serialize message field [cmd]
    bufferOffset = _serializer.string(obj.cmd, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type evaluateSLAMEvoRequest
    let len;
    let data = new evaluateSLAMEvoRequest(null);
    // Deserialize message field [cmd]
    data.cmd = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.cmd);
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'learning_tf2/evaluateSLAMEvoRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '43a54fa49066cddcf148717d9d4a6353';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string cmd
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new evaluateSLAMEvoRequest(null);
    if (msg.cmd !== undefined) {
      resolved.cmd = msg.cmd;
    }
    else {
      resolved.cmd = ''
    }

    return resolved;
    }
};

class evaluateSLAMEvoResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.rmse = null;
    }
    else {
      if (initObj.hasOwnProperty('rmse')) {
        this.rmse = initObj.rmse
      }
      else {
        this.rmse = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type evaluateSLAMEvoResponse
    // Serialize message field [rmse]
    bufferOffset = _serializer.float32(obj.rmse, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type evaluateSLAMEvoResponse
    let len;
    let data = new evaluateSLAMEvoResponse(null);
    // Deserialize message field [rmse]
    data.rmse = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'learning_tf2/evaluateSLAMEvoResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '64ede1f40ef1c350e70bba074ccc7da2';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 rmse
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new evaluateSLAMEvoResponse(null);
    if (msg.rmse !== undefined) {
      resolved.rmse = msg.rmse;
    }
    else {
      resolved.rmse = 0.0
    }

    return resolved;
    }
};

module.exports = {
  Request: evaluateSLAMEvoRequest,
  Response: evaluateSLAMEvoResponse,
  md5sum() { return '35874a05cfbf0d3305ff4de33999af1f'; },
  datatype() { return 'learning_tf2/evaluateSLAMEvo'; }
};
