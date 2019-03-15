const sum = require('./canvas_script');

test('adds 1 + 2 to equal 3', () => {
	const input = {};
	const name = "test";
	input[name]["name"] = "something";
	input[name]["mandatory"] = true;
	const temp_rectangle = new paper.Path.Rectangle(50,50,100,100);
	input[name]["object"] = temp_rectangle;
	const output = {"something":{"x1":50,"y1":50,"x2":150,"y2":150,"mandatory":true}};
	expect(convert_to_save_format(input).toBe(output));
  
});