package src.factories;

import src.factories.common.Animal;
import src.factories.common.Dog;
import src.factories.common.Plant;
import src.factories.common.Tree;

class AbstractFactoryOne implements AbstractFactory {
    public Animal createAnimal() {
        return new Dog();
    }

    public Plant createPlant() {
        return new Tree();
    }
}
