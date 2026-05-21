const mongoose = require('mongoose');

const photoSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    url: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      default: '',
    },
    description: {
      type: String,
      default: '',
    },
    caption: {
      type: String,
      default: '',
    },
    tags: [String],
    energy: {
      type: String,
      enum: ['high', 'medium', 'low'],
      default: 'medium',
    },
    isPublic: {
      type: Boolean,
      default: false,
    },
    createdAt: {
      type: Date,
      default: Date.now,
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Photo', photoSchema);
