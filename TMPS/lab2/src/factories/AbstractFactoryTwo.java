package src.factories;

import src.factories.common.Animal;
import src.factories.common.Cat;
import src.factories.common.Flower;
import src.factories.common.Plant;

class AbstractFactoryTwo implements AbstractFactory {
    public Animal createAnimal() {
        return new Cat();
    }

    public Plant createPlant() {
        return new Flower();
    }
}