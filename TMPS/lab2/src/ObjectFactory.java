package src;

@FunctionalInterface
interface ObjectFactory<T> {
    T createObject();
}
