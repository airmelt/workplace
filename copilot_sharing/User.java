public class User {
    /* 
    用户名: user.name
    用户 id: user.id
    用户年龄: user.age
    用户职业: user.career
    */
    private String name;
    private int id;
    private int age;
    private String career;

    public User(String name, int id, int age, String career) {
        this.name = name;
        this.id = id;
        this.age = age;
        this.career = career;
    }
}