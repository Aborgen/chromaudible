class MusicPlayer {
  constructor(context, frequencyTimePairs) {
    this.context = context;
    this.frequencyTimePairs = frequencyTimePairs;
    this.lastFrequencyPair = [];
    this.scheduleAhead = 0.1/*s*/;
    this.cooldownPeriod = 25/*ms*/;
    this.isFinished = false;
    this.notePtr = 0;
    [this.instrument, this.gainNode] = this.initInstrument();
  }

  initInstrument() {
    // Initialize oscillator
    const osc = this.context.createOscillator();
    osc.frequency.setValueAtTime(0, this.context.currentTime);
    osc.connect(this.context.destination);
    // Initialize oscillator gain
    const gainNode = this.context.createGain();
    gainNode.gain.setValueAtTime(0.3, this.context.currentTime);
    osc.connect(gainNode);
    gainNode.connect(this.context.destination);
    return [osc, gainNode];
  }
  
  instrumentOn() {
    this.instrument.start(this.context.currentTime);
  }

  instrumentOff() {
    this.instrument.stop(this.context.currentTime);
    this.instrument = this.initInstrument();
  }

  setGain(n, timestamp) {
    if (n < -1.0 || n > 1.0) {
      return;
    }

    this.gainNode.gain.setTargetAtTime(n, timestamp, 0.015);
  }

  tuneInstrument(hz, timestamp) {
    if (this.instrument.frequency.value == hz) {
      return;
    }

    this.instrument.frequency.setValueAtTime(hz, timestamp);
  }
  
  nextNote() {
    if (this.notePtr >= this.frequencyTimePairs.length - 1) {
      this.isFinished = true;
      this.instrumentOff();
      return [Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY];
    }

    return this.frequencyTimePairs[this.notePtr++];
  }

  // Based on Chris Wilson's metronome scheduler:
  // https://www.html5rocks.com/en/tutorials/audio/scheduling/
  scheduler() {
    if (this.isFinished) {
      return;
    }

    let timestamp, hz;
    if (this.lastFrequencyPair.length != 0) {
      [timestamp, hz] = this.lastFrequencyPair;
      this.lastFrequencyPair = [];
    }
    else {
      [timestamp, hz] = this.nextNote();
    }

    while (timestamp < this.context.currentTime + this.scheduleAhead) {
      this.tuneInstrument(hz, timestamp);
      [timestamp, hz] = this.nextNote();
    }
    // Context is suspended at construction, freezing currentTime at 0,
    // and enabling scheduling of notes at 0 seconds.
    if (this.context.state == 'suspended') {
      this.context.resume();
    }

    this.lastFrequencyPair = [timestamp, hz];
    window.setTimeout(this.scheduler.bind(this), this.cooldownPeriod);
  }

  play() {
    this.instrumentOn();
    this.scheduler();
    return;
  }
}

export default MusicPlayer;
