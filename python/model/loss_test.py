import torch

from model.loss import (
	consecutive_steps_penalty,
	zero_length_penalty,
	malformed_penalty,
)

ID2TOKEN = {
	0x0: 'STEP',
	0x1: 'NOTE',
	0x2: 'PAD',

	0x10: 'B0',
	0x11: 'B1',

	0x20: 'T0',
	0x21: 'T1',

	0x30: 'D0',
	0x31: 'D12',

	0x40: 'P60',
}

def test__consecutive_steps_penalty__no_penalty():
	target = torch.tensor([[
		0x0, 0x11, 0x20,
		0x1, 0x31, 0x40,
		0x0, 0x11, 0x20,
	]])
	assert consecutive_steps_penalty(target, ID2TOKEN) == 0.0


def test__consecutive_steps_penalty__one_penalty():
	target = torch.tensor([[
		0x0, 0x11, 0x20,
		0x0, 0x11, 0x20,
		0x1, 0x31, 0x40,
	]])
	assert consecutive_steps_penalty(target, ID2TOKEN) == 1.0


def test__consecutive_steps_penalty__two_penalties():
	target = torch.tensor([[
		0x0, 0x11, 0x20,
		0x0, 0x11, 0x20,
		0x0, 0x11, 0x20,
		0x1, 0x31, 0x40,
	]])
	assert consecutive_steps_penalty(target, ID2TOKEN) == 4.0


def test__zero_length_note_penalty__no_penalty():
	target = torch.tensor([[
		0x1, 0x31, 0x40,
		0x1, 0x31, 0x40,
	]])
	assert zero_length_penalty(target, ID2TOKEN) == 0.0


def test__zero_length_note_penalty__one_penalty():
	target = torch.tensor([[
		0x1, 0x30, 0x40,
		0x1, 0x31, 0x40,
	]])
	assert zero_length_penalty(target, ID2TOKEN) == 1.0


def test__zero_length_note_penalty__two_penalties():
	target = torch.tensor([[
		0x1, 0x30, 0x40,
		0x1, 0x30, 0x40,
	]])
	assert zero_length_penalty(target, ID2TOKEN) == 4.0


def test__zero_length_step_penalty__no_penalty():
	target = torch.tensor([[
		0x0, 0x11, 0x20,
		0x1, 0x31, 0x40,
	]])
	assert zero_length_penalty(target, ID2TOKEN) == 0.0


def test__zero_length_step_penalty__one_penalty():
	target = torch.tensor([[
		0x0, 0x10, 0x20,
		0x1, 0x31, 0x40,
	]])
	assert zero_length_penalty(target, ID2TOKEN) == 1.0


def test__malformed_penalty__no_penalty():
	target = torch.tensor([[
		0x0, 0x11, 0x20,
		0x1, 0x31, 0x40,
	]])
	assert malformed_penalty(target, ID2TOKEN) == 0.0


def test__malformed_penalty__one_penalty__start():
	target = torch.tensor([[
		0x0, 0x11, 0x20, 0x20,
		0x1, 0x31, 0x40,
	]])
	assert malformed_penalty(target, ID2TOKEN) == 1.0


def test__malformed_penalty__one_penalty__middle():
	target = torch.tensor([[
		0x0, 0x11, 0x20,
		0x1, 0x31, 0x40, 0x20,
		0x0, 0x11, 0x20,
	]])
	assert malformed_penalty(target, ID2TOKEN) == 1.0


def test__malformed_penalty__one_penalty__end():
	target = torch.tensor([[
		0x0, 0x11, 0x20,
		0x1, 0x31, 0x40, 0x40,
	]])
	assert malformed_penalty(target, ID2TOKEN) == 1.0
