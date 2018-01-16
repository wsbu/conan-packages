#include <gtest/gtest.h>
#include <gmock/gmock.h>

using ::testing::Return;

class Foo {
    public:
        virtual ~Foo () {}

        virtual int foo () = 0;
};

class MockFoo: public Foo {
    public:
        virtual ~MockFoo () {}

        MOCK_METHOD0(foo, int(void));
};

class FooTest: public ::testing::Test {
    protected:
        MockFoo foo;
};

TEST_F(FooTest, FirstTest) {
    EXPECT_CALL(this->foo, foo())
            .WillRepeatedly(Return(42));
    ASSERT_EQ(42, this->foo.foo());
}
