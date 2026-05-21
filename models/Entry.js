const mongoose = require('mongoose');

const entrySchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    content: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      enum: ['intention', 'ritual', 'reflection', 'manifestation'],
      default: 'manifestation',
    },
    energy: {
      type: String,
      enum: ['high', 'medium', 'low'],
      default: 'medium',
    },
    tags: [String],
    images: [String],
    isPublic: {
      type: Boolean,
      default: false,
    },
    createdAt: {
      type: Date,
      default: Date.now,
    },
    updatedAt: {
      type: Date,
      default: Date.now,
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Entry', entrySchema);
