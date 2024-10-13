package src.notfactories;

@FunctionalInterface
interface ObjectFactory<T> {
    T createObject();
}