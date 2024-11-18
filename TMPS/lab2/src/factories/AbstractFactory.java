package src.factories;

import src.factories.common.Animal;
import src.factories.common.Plant;

interface AbstractFactory {
    Animal createAnimal();
    Plant createPlant();
}