#include "blog.h"
#include "config.h"
// blog_generator_beg
extern blog blog_cate1_s1;
extern blog blog_cate2_redirect;
extern blog blog_cate2_paged_attn;
extern blog blog_cate2_language;

void blog_generate(){
	vector<blog> blogvec {
		blog_cate1_s1,
		blog_cate2_redirect,
		blog_cate2_paged_attn,
		blog_cate2_language,
	};
	extern void generate_blog_index(vector<blog>&);
	generate_blog_index(blogvec);
}
// blog_generator_end

int main()
{
	blog_generate();
}

















































