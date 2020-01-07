

class MusicPlayer {
  constructor(context, frequencyTimePairs) {
    this.context = context;
    this.frequencyTimePairs = frequencyTimePairs;
    this.noteLength = 50/*ms*/;
    this.scheduleAhead = 100/*ms*/;
    this.cooldownPeriod = 20/*ms*/;
    this.isFinished = false;
  }

  scheduleNote(hz, timestamp, length) {
    const osc = this.context.createOscillator();
    osc.frequency.value = hz;
    osc.start(timestamp);
    osc.stop(timestamp + length);
  }

  scheduler() {
    if (this.isFinished) {
      return;
    }

    let [hz, timestamp] = this.nextNote();
    while (timestamp < this.context.currentTime + this.scheduleAhead) {
      this.scheduleNote(hz, timestamp, this.noteLength);
      [hz, timestamp] = this.nextNote();
    }

    window.setTimeout(this.scheduler, this.cooldownPeriod);
  }

  nextNote() {
    if (this.frequencyTimePairs.length == 0) {
      this.isFinished = true;
      return [Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY];
    }

    return this.frequencyTimePairs.shift();
  }

  play() {
    this.scheduler();
    return 'Done playing!';
  }
}

export default MusicPlayer;
