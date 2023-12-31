// C program for Red-Black Tree insertion
#include<stdio.h>
#include<stdlib.h>

//A Red-Black tree node structure
#define MAX_MODULE 16

extern struct stack __profile__S;//record funcID

extern struct stack __profile__module_stack;

extern struct stack __profile__shell_time; 

struct fatherNode
{
	unsigned int fatherID;
	unsigned long long accTime[MAX_MODULE];  //根据下标确定module
	unsigned long long times[MAX_MODULE];   //根据下标确定module
	unsigned long long shelltime[MAX_MODULE];    //计时函数时间
};

struct node
{
    struct fatherNode data;
    char color;
    struct node *left, *right, *parent;
};


// Left Rotation
void LeftRotate(struct node **root,struct node *x)
{
    if (!x || !x->right)
        return ;
    //y stored pointer of right child of x
    struct node *y = x->right;

    //store y's left subtree's pointer as x's right child
    x->right = y->left;

    //update parent pointer of x's right
    if (x->right != NULL)
        x->right->parent = x;

    //update y's parent pointer
    y->parent = x->parent;

    // if x's parent is null make y as root of tree
    if (x->parent == NULL)
        (*root) = y;

    // store y at the place of x
    else if (x == x->parent->left)
        x->parent->left = y;
    else    x->parent->right = y;

    // make x as left child of y
    y->left = x;

    //update parent pointer of x
    x->parent = y;
}


// Right Rotation (Similar to LeftRotate)
void rightRotate(struct node **root,struct node *y)
{
    if (!y || !y->left)
        return ;
    struct node *x = y->left;
    y->left = x->right;
    if (x->right != NULL)
        x->right->parent = y;
    x->parent =y->parent;
    if (x->parent == NULL)
        (*root) = x;
    else if (y == y->parent->left)
        y->parent->left = x;
    else y->parent->right = x;
    x->right = y;
    y->parent = x;
}

// Utility function to fixup the Red-Black tree after standard BST insertion
void insertFixUp(struct node **root,struct node *z)
{
    // iterate until z is not the root and z's parent color is red
    while (z != *root && z != (*root)->left && z != (*root)->right && z->parent->color == 'R')
    {
        struct node *y;

        // Find uncle and store uncle in y
        if (z->parent && z->parent->parent && z->parent == z->parent->parent->left)
            y = z->parent->parent->right;
        else
            y = z->parent->parent->left;

        // If uncle is RED, do following
        // (i)  Change color of parent and uncle as BLACK
        // (ii) Change color of grandparent as RED
        // (iii) Move z to grandparent
        if (!y)
            z = z->parent->parent;
        else if (y->color == 'R')
        {
            y->color = 'B';
            z->parent->color = 'B';
            z->parent->parent->color = 'R';
            z = z->parent->parent;
        }

        // Uncle is BLACK, there are four cases (LL, LR, RL and RR)
        else
        {
            // Left-Left (LL) case, do following
            // (i)  Swap color of parent and grandparent
            // (ii) Right Rotate Grandparent
            if (z->parent == z->parent->parent->left &&
                z == z->parent->left)
            {
                char ch = z->parent->color ;
                z->parent->color = z->parent->parent->color;
                z->parent->parent->color = ch;
                rightRotate(root,z->parent->parent);
            }

            // Left-Right (LR) case, do following
            // (i)  Swap color of current node  and grandparent
            // (ii) Left Rotate Parent
            // (iii) Right Rotate Grand Parent
            if (z->parent && z->parent->parent && z->parent == z->parent->parent->left &&
                z == z->parent->right)
            {
                char ch = z->color ;
                z->color = z->parent->parent->color;
                z->parent->parent->color = ch;
                LeftRotate(root,z->parent);
                rightRotate(root,z->parent->parent);
            }

            // Right-Right (RR) case, do following
            // (i)  Swap color of parent and grandparent
            // (ii) Left Rotate Grandparent
            if (z->parent && z->parent->parent &&
                z->parent == z->parent->parent->right &&
                z == z->parent->right)
            {
                char ch = z->parent->color ;
                z->parent->color = z->parent->parent->color;
                z->parent->parent->color = ch;
                LeftRotate(root,z->parent->parent);
            }

            // Right-Left (RL) case, do following
            // (i)  Swap color of current node  and grandparent
            // (ii) Right Rotate Parent
            // (iii) Left Rotate Grand Parent
            if (z->parent && z->parent->parent && z->parent == z->parent->parent->right &&
                z == z->parent->left)
            {
                char ch = z->color ;
                z->color = z->parent->parent->color;
                z->parent->parent->color = ch;
                rightRotate(root,z->parent);
                LeftRotate(root,z->parent->parent);
            }
        }
    }
    (*root)->color = 'B'; //keep root always black
}

// Utility function to insert newly node in RedBlack tree
void insert(struct node **root, struct fatherNode data)
{
    // Allocate memory for new node
    struct node *z = (struct node*)malloc(sizeof(struct node));
    z->data = data;
    z->left = z->right = z->parent = NULL;

     //if root is null make z as root
    if (*root == NULL)
    {
        z->color = 'B';
        (*root) = z;
    }
    else
    {
        struct node *y = NULL;
        struct node *x = (*root);

        // Follow standard BST insert steps to first insert the node
        while (x != NULL)
        {
            y = x;
            if (z->data.fatherID < x->data.fatherID)
                x = x->left;
            else
                x = x->right;
        }
        z->parent = y;
        if (z->data.fatherID > y->data.fatherID)
            y->right = z;
        else
            y->left = z;
        z->color = 'R';

        // call insertFixUp to fix reb-black tree's property if it
        // is voilated due to insertion.
        insertFixUp(root,z);
    }
}

// A utility function to traverse Red-Black tree in inorder fashion
void inorder(struct node *root,int funcid,FILE *fw)
{
    //static int last = 0;
    if (root == NULL)
        return;
    inorder(root->left,funcid,fw);
	
    //struct fatherNode node;
	//node=root->data;
	fprintf(fw,"%d,%d,",funcid,root->data.fatherID);//,%llu,%llu\n,node.times,node.accTime/2
	for(int i=0;i<16;i++)
	{
		fprintf(fw,"%llu,%llu,%llu,",root->data.times[i],root->data.accTime[i]/2,root->data.shelltime[i]/2);
	}
	fprintf(fw,"\n");
	
    //if (root->data.fatherID < last)
    //   printf("\nPUTE\n");
    //last = root->data.fatherID;
    inorder(root->right,funcid,fw);
}
unsigned long long eax, edx;
unsigned long long module_num;
unsigned long long func_begin_time;
int search(struct node *T,int data,int ans,unsigned long long b){
    if(T!=NULL ){
        if(T->data.fatherID<data)
            ans=search(T->right,data,ans,b);
        else if(T->data.fatherID>data)
            ans=search(T->left,data,ans,b);
        else
		{
			if(T->data.fatherID==data)
			{
				
				T->data.times[__profile__module_stack.sta[__profile__module_stack.top]]++;
				asm volatile("rdtsc\n\t": "=a" (eax), "=d" (edx));
				T->data.accTime[__profile__module_stack.sta[__profile__module_stack.top]]+=((unsigned long long)eax | (unsigned long long)edx << 32) - b;
				
				//shelltimeend and record
				module_num=__profile__module_stack.sta[__profile__module_stack.top];
				pop(&__profile__S);
				
				func_begin_time=pop(&__profile__shell_time);
				asm volatile("rdtsc\n\t": "=a" (eax), "=d" (edx));
				T->data.shelltime[module_num]+=(((unsigned long long)eax | (unsigned long long)edx << 32) - func_begin_time);
			
				return 1;
			}
			else
			{
				return 0;
			}
				
			//printf("%d\n",T==nil ? 0: 1);
			//return T==nil ? 0: 1;
		}
            
    }
	return ans;
}