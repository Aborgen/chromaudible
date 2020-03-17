const StatusEnum = Object.freeze(
  {
    'NOT_STARTED' : 1,
    'PLAYING': 2,
    'PAUSED': 3,
    'FINISHED': 4
  }
);

class MusicPlayer {
  constructor(context, frequencyTimePairs, gainTimePairs, timbreTexture, cleanupFunction) {
    this.context = context;
    this.frequencyTimePairs = frequencyTimePairs;
    this.gainTimePairs = gainTimePairs;
    this.timbreTexture = timbreTexture;

    this.lastFrequencyPair = [];
    this.queuedGainChange = [];
    this.scheduleAhead = 0.1/*s*/;
    this.cooldownPeriod = 25/*ms*/;
    this.status = StatusEnum.NOT_STARTED;
    this.notePtr = 0;
    this.gainPtr = 0;
    [this.instrument, this.gainNode] = this.initInstrument();
    this.closeOnTime(cleanupFunction);
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
    [this.instrument, this.gainNode] = this.initInstrument();
  }

  setGain(timestamp, n) {
    if (n < -1.0 || n > 1.0) {
      return;
    }

    this.gainNode.gain.setTargetAtTime(n, timestamp, 0.015);
  }

  tuneInstrument(hz, timestamp) {
    if (this.queuedGainChange[0] === timestamp) {
      this.setGain(...this.queuedGainChange);
      this.queuedGainChange = this.nextGainChange();
    }

    if (this.instrument.frequency.value === hz) {
      return;
    }

    this.instrument.frequency.setValueAtTime(hz, timestamp);
  }

  nextNote() {
    if (this.notePtr >= this.frequencyTimePairs.length - 1) {
      this.status === StatusEnum.FINISHED;
      return [Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY];
    }

    return this.frequencyTimePairs[this.notePtr++];
  }

  nextGainChange() {
   if (this.gainPtr >= this.gainTimePairs.length - 1) {
      return [Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY];
    }

    return this.gainTimePairs[this.gainPtr++];
  }

  // Based on Chris Wilson's metronome scheduler:
  // https://www.html5rocks.com/en/tutorials/audio/scheduling/
  scheduler() {
    if (this.status === StatusEnum.PAUSED ||
        this.status === StatusEnum.FINISHED) {
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
    if (this.status === StatusEnum.NOT_STARTED) {
      this.instrumentOn();
      this.context.resume();
      this.status = StatusEnum.PLAYING;
    }

    this.lastFrequencyPair = [timestamp, hz];
    window.setTimeout(this.scheduler.bind(this), this.cooldownPeriod);
  }

  closeOnTime(cleanupFunction) {
    const stopTime = this.frequencyTimePairs[this.frequencyTimePairs.length - 1][0];
    const i = setInterval(() => {
      if (this.context.currentTime >= stopTime) {
        clearInterval(i);
        this.instrumentOff();
        this.context.close();
        cleanupFunction();
      }
    }, 1000);
  }

  play() {
    this.instrumentOn();
    this.scheduler();
    return;
  }
}

export { MusicPlayer, StatusEnum };
