#include "PhotoResistor.h"

PhotoResistor::PhotoResistor(uint8_t _pin, float _voltRef, float _adcResolution,
                           float _minVolt, float _maxVolt, float _minLux, float _maxLux) {
    pin = _pin;
    voltRef = _voltRef;
    adcResolution = _adcResolution;
    minVolt = _minVolt;
    maxVolt = _maxVolt;
    minLux = _minLux;
    maxLux = _maxLux;
}

void PhotoResistor::begin() {
  pinMode(pin, INPUT);
}

uint16_t PhotoResistor::readRawValue() {
  return analogRead(pin);
}

float PhotoResistor::convertADCToVoltage(uint16_t adcValue) {
  return (adcValue / this->adcResolution) * this->voltRef;
}

float PhotoResistor::convertVoltageToLux(float voltage) {
  float lux = (voltage - minVolt) * (maxLux - minLux) / (maxVolt - minVolt) + minLux;
  
  // Apply saturation
  if (lux < minLux) {
    lux = minLux;
  } else if (lux > maxLux) {
      lux = maxLux;
  }
  
  return lux;
}

float PhotoResistor::readLux() {
  uint16_t rawValue = readRawValue();
  float voltage = convertADCToVoltage(rawValue);
  return convertVoltageToLux(voltage);
}